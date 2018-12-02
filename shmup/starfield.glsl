---vertex
$HEADER$

attribute vec2  vCenter;
attribute float vScale;

void main(void)
{
    // multiply relative coordinates of all vertices by factor of vScale
    // to resize the mesh proportionally, then translating them to the position
    // by vCenter attribute
    tex_coord0 = vTexCoords0;
    mat4 move_mat = mat4
         (1.0, 0.0, 0.0, vCenter.x,
         0.0, 1.0, 0.0, vCenter.y,
         0.0, 0.0, 1.0, 0.0,
         0.0, 0.0, 0.0, 1.0);
    vec4 pos = vec4(vPosition.xy * vScale, 0.0, 1.0) * move_mat;
    gl_Position = projection_mat * modelview_mat * pos;
}

---fragment
$HEADER$

void main(void)
{
    gl_FragColor = texture2D(texture0, tex_coord0);
}