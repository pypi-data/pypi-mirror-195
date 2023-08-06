#define PY_SSIZE_T_CLEAN
#include "Python.h"

static PyObject *
_pyminmax_minmax(PyObject *self, PyObject *args, PyObject *kwds)
{
    PyObject *v, *it, *item, *val, *minitem, *minval, *maxitem, *maxval;
    PyObject *result, *emptytuple, *defaultval = NULL, *keyfunc = NULL;
    static char *kwlist[] = {"key", "default", NULL};
    const char *name = "minmax";
    const int positional = PyTuple_Size(args) > 1;
    int ret;

    if (positional) {
        v = args;
    }
    else if (!PyArg_UnpackTuple(args, name, 1, 1, &v)) {
        if (PyExceptionClass_Check(PyExc_TypeError)) {
            PyErr_Format(PyExc_TypeError,
                         "%s expected at least 1 argument, got 0", name);
        }
        return NULL;
    }

    emptytuple = PyTuple_New(0);
    if (emptytuple == NULL)
        return NULL;
    ret = PyArg_ParseTupleAndKeywords(emptytuple, kwds, "|$OO:minmax", kwlist,
                                      &keyfunc, &defaultval);
    Py_DECREF(emptytuple);
    if (!ret)
        return NULL;

    if (positional && defaultval != NULL) {
        PyErr_Format(PyExc_TypeError,
                     "Cannot specify a default for %s() with multiple "
                     "positional arguments", name);
        return NULL;
    }

    it = PyObject_GetIter(v);
    if (it == NULL) {
        return NULL;
    }

    if (keyfunc == Py_None) {
        keyfunc = NULL;
    }

    minitem = NULL;
    minval = NULL;
    maxitem = NULL;
    maxval = NULL;
    while (( item = PyIter_Next(it) )) {
        if (keyfunc != NULL) {
            val = PyObject_CallOneArg(keyfunc, item);
            if (val == NULL)
                goto Fail_it_item;
        }
        else {
            val = Py_NewRef(item);
        }

        if (minval == NULL) {
            minitem = item;
            minval = val;
            maxitem = Py_NewRef(item);
            maxval = Py_NewRef(val);
        }
        else {
            int cmp_mx = PyObject_RichCompareBool(val, maxval, Py_GT);
            int cmp_mn = PyObject_RichCompareBool(val, minval, Py_LT);

            if (cmp_mx < 0 || cmp_mn < 0) {
                goto Fail_it_item_and_val;
            }
            else if (cmp_mx > 0) {
                Py_DECREF(maxval);
                Py_DECREF(maxitem);
                maxval = val;
                maxitem = item;
            }
            else if (cmp_mn > 0) {
                Py_DECREF(minval);
                Py_DECREF(minitem);
                minval = val;
                minitem = item;
            }
            else {
                Py_DECREF(item);
                Py_DECREF(val);
            }
        }
    }
    if (PyErr_Occurred()) {
        goto Fail_it;
    }
    if (minval == NULL) {
        if (defaultval != NULL) {
            Py_DECREF(it);
            return Py_NewRef(defaultval);
        } else {
            PyErr_Format(PyExc_ValueError,
                         "%s() iterable argument is empty", name);
            Py_DECREF(it);
            return NULL;
        }
    }
    result = Py_BuildValue("(OO)", minitem, maxitem);
    Py_DECREF(minval);
    Py_DECREF(maxval);
    Py_DECREF(minitem);
    Py_DECREF(maxitem);
    Py_DECREF(it);
    return result;

Fail_it_item_and_val:
    Py_DECREF(val);
Fail_it_item:
    Py_DECREF(item);
Fail_it:
    Py_XDECREF(minval);
    Py_XDECREF(minitem);
    Py_XDECREF(maxval);
    Py_XDECREF(maxitem);
    Py_DECREF(it);
    return NULL;
}

PyDoc_STRVAR(minmax_doc,
"minmax(iterable, *[, default=obj, key=func]) -> (minitem, maxitem)\n\
minmax(arg1, arg2, *args, *[, key=func]) -> (minitem, maxitem)\n\n\
With a single iterable argument, return its smallest and largest item as a \n\
pair. The default keyword-only argument specifies an object to return if the\n\
provided iterable is empty.\n\n\
With two or more arguments, return the smallest and largest argument.");

static PyMethodDef _pyminmax_methods[] = {
    {"minmax", (PyCFunction)(void(*)(void))_pyminmax_minmax, METH_VARARGS |
                                                             METH_KEYWORDS,
                                                             minmax_doc},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef _pyminmaxmodule = {
    .m_base = PyModuleDef_HEAD_INIT,
    .m_name = "_pyminmax",
    .m_doc = NULL,
    .m_size = -1,
    .m_methods = _pyminmax_methods
};

PyMODINIT_FUNC
PyInit__pyminmax(void)
{
    return PyModule_Create(&_pyminmaxmodule);
}
