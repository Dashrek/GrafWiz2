vertex_src = """
# version 330
layout(location = 0) in vec3 a_position;
layout(location = 1) in vec2 a_texture;
layout(location = 2) in vec3 a_normal;
uniform mat4 model;
uniform mat4 projection;
uniform mat4 view;
uniform mat4 light;
out vec2 v_texture;
out vec3 frag_normal;
void main()
{   
    frag_normal=(light*vec4(a_normal,0.0f)).xyz;
    gl_Position = projection * view * model * vec4(a_position, 1.0);
    v_texture = a_texture;
}
"""

fragment_src = """
# version 330
in vec2 v_texture;
in vec3 frag_normal;
out vec4 out_color;
uniform sampler2D s_texture;
void main()
{
    vec3 ambientLightIntensity = vec3(0.3f, 0.3f, 0.3f);
    vec3 sunLightIntensity = vec3(0.9f, 0.9f, 0.9f);
    vec3 sunLightDirection = normalize(vec3(-2.0f, -2.0f, 0.0f));
    vec4 texel = texture(s_texture, v_texture);
    vec3 lightIntensity = ambientLightIntensity + sunLightIntensity * max(dot(frag_normal, sunLightDirection), 0.0f);
    out_color = vec4(texel.rgb * lightIntensity, texel.a);
    //out_color = texture(s_texture, v_texture);
}
"""
