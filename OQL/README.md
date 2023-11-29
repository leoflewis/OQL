# Object Oriented Query Engine 

## Purpose

If you have ever used the Python SQL connectors, you may have come across a pattern similar to this one below:

```
mycursor.execute("SELECT * FROM customers ORDER BY name")
```

A string containing a SQL query is passed to an .execute() method. There is nothing wrong with this inherently, but it can quickly become tedious to manage queries if one is trying to build an application that constructs queries on the fly. 

That is where the Object Oriented Query Engine comes in. 

## Details

The Object Oriented Query Engine uses Python v3.10.6 to define several classes and related functions that allows Python developers to build SQL queries through an Object Oriented model.

## Syntax

### New Instance
A new instance of a Query object can be defined as follows:

```
query = Query("tablename")
```
Resulting query:
```
SELECT * FROM tablename;
```

### Selecting Attributes
Attributes to be selected can be specified through the Select() function. If attributes are not specified, all will be selected.
```
query.Select("attribute1")
```
Resulting query:
```
SELECT attribute1 FROM tablename;
```
Additionally, the table name (or alias) that the attribute corresponds to can be specified.
```
query.Select("attribute1", "tablename")
```
Resulting query:
```
SELECT tablename.attribute1 FROM tablename;
```

### Conditions
