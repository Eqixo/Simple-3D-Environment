#version 330 core 

in vec3 Normal; 
in vec3 FragPos; 
in vec3 Color; 
in vec3 LightDir; 
in vec3 AmbientLight; 
in float FogFactor;

out vec4 FragColor;

uniform vec3 fogColor;

void main() { 
  // Éclairage diffus 
  float diff = max(dot(normalize(Normal), LightDir), 0.0); 
  vec3 diffuse = diff * Color;

  // Éclairage ambiant
  vec3 ambient = AmbientLight * Color;
  
  // Couleur du terrain
  vec3 terrainColor = ambient + diffuse;
  
  // Mélanger avec la couleur du brouillard
  vec3 finalColor = mix(terrainColor, fogColor, FogFactor);
  
  FragColor = vec4(finalColor, 1.0);
}