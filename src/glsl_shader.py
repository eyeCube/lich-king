'''
'''

from panda3d.core import *

def glsl_shader():
    return Shader.make(Shader.SL_GLSL, """
#version 330

uniform mat4 p3d_ModelViewProjectionMatrix;
uniform mat4 p3d_ModelViewMatrix;
uniform mat3 p3d_NormalMatrix;

in vec4 vertex;
in vec3 normal;

out vec3 vpos;
out vec3 norm;
out vec4 shad[3];

uniform struct {
  vec4 position;
  vec4 diffuse;
  vec4 specular;
  vec3 attenuation;
  vec3 spotDirection;
  float spotCosCutoff;
  float spotExponent;
  sampler2DShadow shadowMap;
  mat4 shadowMatrix;
} p3d_LightSource[3];

void main() {
  gl_Position = p3d_ModelViewProjectionMatrix * vertex;
  vpos = vec3(p3d_ModelViewMatrix * vertex);
  norm = normalize(p3d_NormalMatrix * normal);
  shad[0] = p3d_LightSource[0].shadowMatrix * vertex;
  shad[1] = p3d_LightSource[1].shadowMatrix * vertex;
  shad[2] = p3d_LightSource[2].shadowMatrix * vertex;
}
""", """
#version 330

uniform sampler2D p3d_Texture0;

uniform struct {
  vec4 ambient;
} p3d_LightModel;

uniform struct {
  vec4 ambient;
  vec4 diffuse;
  vec3 specular;
  float shininess;
} p3d_Material;

uniform struct {
  vec4 position;
  vec4 diffuse;
  vec4 specular;
  vec3 attenuation;
  vec3 spotDirection;
  float spotCosCutoff;
  float spotExponent;
  sampler2DShadow shadowMap;
  mat4 shadowMatrix;
} p3d_LightSource[3];

in vec3 vpos;
in vec3 norm;
in vec4 shad[3];

out vec4 p3d_FragColor;

void main() {
  p3d_FragColor = p3d_LightModel.ambient * p3d_Material.ambient;

  for (int i = 0; i < p3d_LightSource.length(); ++i) {
    vec3 diff = p3d_LightSource[i].position.xyz - vpos * p3d_LightSource[i].position.w;
    vec3 L = normalize(diff);
    vec3 E = normalize(-vpos);
    vec3 R = normalize(-reflect(L, norm));
    vec4 diffuse = clamp(p3d_Material.diffuse * p3d_LightSource[i].diffuse * max(dot(norm, L), 0), 0, 1);
    vec4 specular = vec4(p3d_Material.specular, 1) * p3d_LightSource[i].specular * pow(max(dot(R, E), 0), p3d_Material.shininess);

    float spotEffect = dot(normalize(p3d_LightSource[i].spotDirection), -L);

    if (spotEffect > p3d_LightSource[i].spotCosCutoff) {
      diffuse *= pow(spotEffect, p3d_LightSource[i].spotExponent);
      diffuse *= textureProj(p3d_LightSource[i].shadowMap, shad[i]);
      p3d_FragColor += diffuse / dot(p3d_LightSource[i].attenuation, vec3(1, length(diff), length(diff) * length(diff)));
    }
  }

  p3d_FragColor.a = 1;
}
""")
