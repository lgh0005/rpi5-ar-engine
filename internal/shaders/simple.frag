#version 310 es
precision highp float;

struct Material 
{
    sampler2D albedo_map;
    sampler2D specular_map;
    sampler2D normal_map;
    sampler2D height_map;
    sampler2D emission_map;
    float shininess;
    float emission_intensity;
    float height_scale;
};

uniform Material u_material;

in vec3 vPos;
in vec3 vNormal;
in vec2 vTexCoord;
in mat3 vTBN;

out vec4 FragColor;

uniform vec3 u_view_pos;

// 조명 설정 (임시)
vec3 lightDir = normalize(vec3(1.0, 1.0, 1.0));
vec3 lightColor = vec3(1.0, 1.0, 1.0);
float ambientStrength = 0.2;

// Parallax Mapping 함수 (임시)
// 뷰 방향과 높이맵을 이용해 UV 좌표를 오프셋시킵니다.
vec2 ParallaxMapping(vec2 texCoords, vec3 viewDir)
{
    float height = texture(u_material.height_map, texCoords).r;
    vec2 p = viewDir.xy * (height * u_material.height_scale);
    return texCoords - p;
}

void main() 
{
    // 0. Parallax Mapping 준비
    vec3 viewDir = normalize(u_view_pos - vPos);
    vec3 viewDirTS = transpose(vTBN) * viewDir;
    vec2 texCoords = ParallaxMapping(vTexCoord, viewDirTS);
    if (texCoords.x > 1.0 || texCoords.y > 1.0 || texCoords.x < 0.0 || texCoords.y < 0.0) 
        discard;

    // 1. Albedo (변경된 texCoords 사용)
    vec4 albedo = texture(u_material.albedo_map, texCoords);
    if(albedo.a < 0.1) discard; 

    // 2. Normal Mapping (변경된 texCoords 사용)
    vec3 mapNorm = texture(u_material.normal_map, texCoords).rgb;
    vec3 norm = normalize(mapNorm * 2.0 - 1.0); 
    norm = normalize(vTBN * norm); 

    // 3. Ambient
    vec3 ambient = ambientStrength * lightColor;

    // 4. Diffuse
    float diff = max(dot(norm, lightDir), 0.0);
    vec3 diffuse = diff * lightColor;

    // 5. Specular (Blinn-Phong)
    vec3 halfwayDir = normalize(lightDir + viewDir);
    float spec = pow(max(dot(norm, halfwayDir), 0.0), u_material.shininess);
    float specularStrength = texture(u_material.specular_map, texCoords).r;
    vec3 specular = specularStrength * spec * lightColor;

    // 6. Emission
    vec3 emission = texture(u_material.emission_map, texCoords).rgb;
    emission *= u_material.emission_intensity;

    // 최종 결과물
    vec3 result = (ambient + diffuse + specular) * albedo.rgb + emission;
    FragColor = vec4(result, albedo.a);
}