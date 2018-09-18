#version 400

in vec2 v_UV;

uniform sampler2D u_Texture;

void main() {
    gl_FragColor = texture2D(u_Texture, v_UV);
}
