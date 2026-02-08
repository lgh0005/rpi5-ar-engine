#version 310 es

layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aNormal;
layout (location = 2) in vec2 aTexCoord;
layout (location = 3) in vec3 aTangent;

out vec3 vPos;
out vec3 vNormal;
out vec2 vTexCoord;
out mat3 vTBN;

uniform mat4 u_model;
uniform mat4 u_view;
uniform mat4 u_projection;
uniform mat4 u_normal_matrix;

void main() 
{
    // 월드 공간에서의 정점 위치 계산
    vec4 worldPos = u_model * vec4(aPos, 1.0);
    vPos = worldPos.xyz;
    vTexCoord = aTexCoord;

    // 노멀 행렬을 이용한 법선 및 탄젠트 변환
    vec3 T = normalize(vec3(u_normal_matrix * vec4(aTangent, 0.0)));
    vec3 N = normalize(vec3(u_normal_matrix * vec4(aNormal, 0.0)));
    T = normalize(T - dot(T, N) * N); // 그람-슈미트 직교화
    vec3 B = cross(N, T);

    vNormal = N;
    vTBN = mat3(T, B, N);

    gl_Position = u_projection * u_view * worldPos;
}