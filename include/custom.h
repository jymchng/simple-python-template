#ifndef CUSTOM_H
#define CUSTOM_H

#include <Python.h>

typedef struct {
    PyObject_HEAD
    PyObject* first; /* first name */
    PyObject* last;  /* last name */
    int number;
} CustomObject;

// Function declarations
static void Custom_dealloc(CustomObject* self);
static PyObject* Custom_new(PyTypeObject* type, PyObject* args, PyObject* kwds);
static int Custom_init(CustomObject* self, PyObject* args, PyObject* kwds);
static PyObject* Custom_name(CustomObject* self, PyObject* Py_UNUSED(ignored));

// Type definition
extern PyTypeObject CustomType;

// Module initialization
PyMODINIT_FUNC PyInit_custom(void);

#endif // CUSTOM_H
