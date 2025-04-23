#version 330 core 

layout(location = 0) in vec3 aPos; 
layout(location = 1) in vec3 aNormal; 
layout(location = 2) in vec3 aColor;

uniform mat4 modelViewMatrix; 
uniform mat4 projectionMatrix; 
uniform vec3 lightPosition; 
uniform vec3 lightColor; 
uniform vec3 ambientLight; 
uniform float fogStart; 
uniform float fogEnd;

out vec3 Normal; 
out vec3 FragPos; 
out vec3 Color; 
out vec3 LightDir; 
out vec3 AmbientLight; 
out float FogFactor;

void main() { 
  gl_Position = projectionMatrix * modelViewMatrix * vec4(aPos, 1.0); 
  FragPos = vec3(modelViewMatrix * vec4(aPos, 1.0)); 
  Normal = mat3(transpose(inverse(modelViewMatrix))) * aNormal; 
  Color = aColor; 
  LightDir = normalize(lightPosition - FragPos); 
  AmbientLight = ambientLight;

  // Calculer la distance pour le brouillard
  float fogDistance = length(FragPos);
  FogFactor = clamp((fogDistance - fogStart) / (fogEnd - fogStart), 0.0, 1.0);
}