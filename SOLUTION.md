# Compound Color Assignment

## Introduction
The purpose of this module is to assign colors to compounds from a predefined palette. The module incorporates a caching mechanism, ensuring that compounds that have not been used for a while receive a new color assignment. However, within specific intervals, the assigned color remains constant.

---

## Product Requirements
This feature is implemented in two versions, both utilizing a simple cached dictionary. The first version employs an external package called `expiringdict`, while the second version is developed internally.

---

## Detailed Design
The objective of this implementation is to generate colors for compounds. To achieve this, a dictionary with time-to-live (TTL) functionality is required. There are multiple existing implementations of dictionaries with expiration features in Python.

In `mailgun_expiringdict` module, I am using [this](https://github.com/mailgun/expiringdict) implementation from the `expiringdict` package. Additionally, I have provided a simple structure called "GPExpiringDict" to serve this purpose. The structure consists of an entry dictionary, where each item contains a color value and an expiration time.

The module offers three public methods:
1. **set_value(self, key, value, ttl=ASSIGNMENT_TTL_SEC):** Assigns a color to the specified compound.
2. **get_value(self, key):** Retrieves the unexpired color assigned to the specified compound. Otherwise, raises KeyError
3. **read_unexpired_entries(self)** Returns all unexpired compound-color assignments stored in the dictionary.

The main driver code can utilize either the `expiringdict` package or the custom `GPExpiringDict` structure as the underlying expiring dictionary. Upon the initial call, an unused color is assigned from the palette. Subsequent calls retrieve the assigned color and update its expiration time.

### Drawback
In systems with a large number of compounds, the `GPExpiringDict` structure may consume more memory since expired assignments are not deleted until a `get_value(self, key):)` call is made.