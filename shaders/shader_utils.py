from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram

def create_shader_program(vertex_path, fragment_path):
    # Charger le code source des shaders
    with open(vertex_path, 'r') as f:
        vertex_source = f.read()
    with open(fragment_path, 'r') as f:
        fragment_source = f.read()

    # Compiler les shaders
    vertex_shader = compileShader(vertex_source, GL_VERTEX_SHADER)
    fragment_shader = compileShader(fragment_source, GL_FRAGMENT_SHADER)

    # Lier le programme
    program = compileProgram(vertex_shader, fragment_shader)

    # Nettoyer les shaders individuels
    glDeleteShader(vertex_shader)
    glDeleteShader(fragment_shader)

    # Vérifier les erreurs de compilation/liaison
    if glGetProgramiv(program, GL_LINK_STATUS) != GL_TRUE:
        raise RuntimeError(glGetProgramInfoLog(program))

    return program