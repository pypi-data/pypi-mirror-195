#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <structmember.h>

#include "ringbuffer.h"

static void
RingBuffer_dealloc(RingBuffer *self)
{
    Py_XDECREF(self->items);
    Py_TYPE(self)->tp_free((PyObject *)self);
}

static PyObject *
RingBuffer_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    RingBuffer *self;

    self = (RingBuffer *)type->tp_alloc(type, 0);
    if (self != NULL)
    {
        self->capacity = 0;
        self->size = 0;
        self->head = 0;
        self->tail = 0;
        self->items = NULL;
    }

    return (PyObject *)self;
}

static int
RingBuffer_init(RingBuffer *self, PyObject *args)
{
    PyObject *capacity = NULL;

    // get capacity from args
    if (!PyArg_ParseTuple(args, "O", &capacity))
        return -1;

    if (!PyLong_Check(capacity))
    {
        PyErr_SetString(PyExc_TypeError, "[TypeError] Capacity must be an integer");
        return -1;
    }

    self->capacity = PyLong_AsLong(capacity);
    self->items = (PyObject **)PyMem_Malloc(self->capacity * sizeof(PyObject *));

    if (self->items == NULL)
    {
        PyErr_SetString(PyExc_MemoryError, "Out of memory");
        return -1;
    }

    return 0;
}

static PyObject *
RingBuffer_is_empty(RingBuffer const *self)
{
    if (self->size == 0)
        Py_RETURN_TRUE;

    Py_RETURN_FALSE;
}

static PyObject *
RingBuffer_is_full(RingBuffer const *self)
{
    if (self->size == self->capacity)
        Py_RETURN_TRUE;

    Py_RETURN_FALSE;
}

static PyObject *
RingBuffer_enqueue(RingBuffer *self, PyObject *args)
{
    // its only works with integers, solve that and make it work with any type
    PyObject *item = NULL;

    if (!PyArg_ParseTuple(args, "O", &item))
        return NULL;
    Py_INCREF(item);

    // if its full, overwrite the oldest item
    if (self->size == self->capacity)
    {
        Py_DECREF(self->items[self->head]);
        self->items[self->head] = item;
        self->head = (self->head + 1) % self->capacity;
        self->tail = (self->tail + 1) % self->capacity;
    }
    else
    {
        self->items[self->tail] = item;
        self->tail = (self->tail + 1) % self->capacity;
        self->size++;
    }

    Py_RETURN_NONE;
}

static PyObject *
RingBuffer_dequeue(RingBuffer *self)
{
    if (self->size == 0)
        Py_RETURN_NONE;

    PyObject *item = self->items[self->head];
    self->items[self->head] = NULL;
    self->head = (self->head + 1) % self->capacity;
    self->size--;

    return item;
}

static PyObject *
RingBuffer_peek(RingBuffer const *self)
{
    if (self->size == 0)
        Py_RETURN_NONE;

    return self->items[self->head];
}

static PyObject *
RingBuffer_size(RingBuffer const *self)
{
    return PyLong_FromLong(self->size);
}

static PyObject *
RingBuffer_capacity(RingBuffer const *self)
{
    return PyLong_FromLong(self->capacity);
}

static PyMemberDef RingBuffer_members[] = {
    {"capacity", T_INT, offsetof(RingBuffer, capacity), 0, "RingBuffer capacity"},
    {"size", T_INT, offsetof(RingBuffer, size), 0, "RingBuffer size"},
    {"head", T_INT, offsetof(RingBuffer, head), 0, "RingBuffer head"},
    {"tail", T_INT, offsetof(RingBuffer, tail), 0, "RingBuffer tail"},
    {NULL} /* Sentinel */
};

static PyMethodDef RingBuffer_methods[] = {
    {"is_empty", (PyCFunction)RingBuffer_is_empty, METH_NOARGS, "Check if the RingBuffer is empty"},
    {"is_full", (PyCFunction)RingBuffer_is_full, METH_NOARGS, "Check if the RingBuffer is full"},
    {"enqueue", (PyCFunction)RingBuffer_enqueue, METH_VARARGS, "Add an item to the RingBuffer"},
    {"dequeue", (PyCFunction)RingBuffer_dequeue, METH_NOARGS, "Remove and return the oldest item from the RingBuffer"},
    {"peek", (PyCFunction)RingBuffer_peek, METH_NOARGS, "Return the oldest item from the RingBuffer"},
    {"size", (PyCFunction)RingBuffer_size, METH_NOARGS, "Return the size of the RingBuffer"},
    {"capacity", (PyCFunction)RingBuffer_capacity, METH_NOARGS, "Return the capacity of the RingBuffer"},
    {NULL} /* Sentinel */
};

PyTypeObject RingBufferType = {
    PyVarObject_HEAD_INIT(NULL, 0)
        .tp_name = "RingBuffer",
    .tp_basicsize = sizeof(RingBuffer),
    .tp_itemsize = 0,
    .tp_new = RingBuffer_new,
    .tp_init = (initproc)RingBuffer_init,
    .tp_dealloc = (destructor)RingBuffer_dealloc,
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_doc = "RingBuffer objects",
    .tp_methods = RingBuffer_methods,
    .tp_members = RingBuffer_members,
};