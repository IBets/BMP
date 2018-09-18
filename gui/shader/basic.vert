#version 400

#define VERT_POSITION   0
#define VERT_TEXT_COORD 1

uniform mat4 u_ModelMatrix;
uniform mat4 u_MVP;



layout (location = VERT_POSITION)   in vec3 VertexPosition;
layout (location = VERT_TEXT_COORD) in vec2 VertexTextCoord;

out vec2 v_UV;

void main()
{
   	
    gl_Position = u_MVP*u_ModelMatrix*vec4(VertexPosition, 1.0); 
    v_UV = VertexTextCoord;
}
