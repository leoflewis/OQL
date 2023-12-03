from Query import *

def TestNewSelectAll():
    q = Query("contact")
    query = q.getQuery()
    print(query)
    exQuery = "SELECT * FROM contact"
    assert query == exQuery

def TestSelectAttributes():
    q = Query("contact")
    q.Select("firstName")
    q.Select("lastName")
    query = q.getQuery()
    print(query)
    exQuery = "SELECT firstName, lastName FROM contact"
    assert query == exQuery

def TestSelectAttributesWithTableName():
    q = Query("contact")
    q.Select("firstName", "contact")
    q.Select("lastName", "contact")
    query = q.getQuery()
    print(query)
    exQuery = "SELECT contact.firstName, contact.lastName FROM contact"
    assert query == exQuery

def TestInnerJoin():
    q = Query("contact")
    q.Join("account", JoinOperators.INNER, "contactid", "contactid")
    query = q.getQuery()
    print(query)
    exQuery = "SELECT * FROM contact INNER JOIN account ON contact.contactid = contactid"
    assert query == exQuery

def TestInnerJoinWithAlias():
    q2 = Query("contact")
    q2.Join("account", JoinOperators.INNER, "contactid", "contactid", "acc")
    query = q2.getQuery()
    print(query)
    exQuery = "SELECT * FROM contact INNER JOIN account AS acc ON contact.contactid = acc.contactid"
    assert query == exQuery

def TestAddCondition():
    q = Query("contact")
    q.addSingleCondition("age", ConditionalOperators.GreaterThan, 50)
    query = q.getQuery()
    print(query)
    exQuery = "SELECT * FROM contact WHERE age > 50"
    assert query == exQuery

def TestAddConditionWithTableName():
    q = Query("contact")
    q.addSingleCondition("age", ConditionalOperators.GreaterThan, 50, "contact")
    query = q.getQuery()
    print(query)
    exQuery = "SELECT * FROM contact WHERE contact.age > 50"
    assert query == exQuery

def TestGroupBySingle():
    q = Query("contact")
    q.Select("lastName")
    q.Select(AggregateFunctions.Count("id"))
    q.GroupBy("lastName")
    query = q.getQuery()
    print(query)
    exQuery = "SELECT lastName, COUNT(id) FROM contact GROUP BY lastName"
    assert query == exQuery

def TestGroupByMultiple():
    q = Query("contact")
    q.Select("lastName")
    q.Select("firstName")
    q.Select(AggregateFunctions.Count("id"))
    q.GroupBy("lastName")
    q.GroupBy("firstName")
    query = q.getQuery()
    print(query)
    exQuery = "SELECT lastName, firstName, COUNT(id) FROM contact GROUP BY lastName, firstName"
    assert query == exQuery

def TestOrderBySingleDesc():
    q = Query("contact")
    q.OrderBy("lastName", Orders.Descending)
    query = q.getQuery()
    print(query)
    exQuery = "SELECT * FROM contact ORDER BY lastName DESC"
    assert query == exQuery

def TestOrderByMultipleDescAndAsc():
    q = Query("contact")
    q.OrderBy("lastName", Orders.Descending)
    q.OrderBy("firstName", Orders.Ascending)
    query = q.getQuery()
    print(query)
    exQuery = "SELECT * FROM contact ORDER BY lastName DESC, firstName ASC"
    assert query == exQuery

def TestConditionSetAND():
    c = ConditionSet(LogicalOperators.And)
    c.addCondition("age", ConditionalOperators.GreaterThan, 50)
    c.addCondition("emailAddress", ConditionalOperators.NotNull)
    condition = (c.getCondition())
    exCondition = "(age > 50 AND emailAddress IS NOT NULL)"
    assert condition == exCondition

def TestConditionSetOR():
    c = ConditionSet(LogicalOperators.Or)
    c.addCondition("age", ConditionalOperators.GreaterThan, 50)
    c.addCondition("emailAddress", ConditionalOperators.NotNull)
    c.addCondition("daysActive", ConditionalOperators.LessThan, 365)
    condition = (c.getCondition())
    exCondition = "(age > 50 OR emailAddress IS NOT NULL OR daysActive < 365)"
    assert condition == exCondition

def TestConditionSetSingle():
    c = ConditionSet(LogicalOperators.And)
    c.addCondition("age", ConditionalOperators.GreaterThan, 50)
    condition = (c.getCondition())
    exCondition = "(age > 50)"
    assert condition == exCondition

def TestConditionSimple():
    inner1 = ConditionSet(LogicalOperators.And)
    inner1.addCondition("age", ConditionalOperators.LessThan, 0)
    inner1.addCondition("length", ConditionalOperators.GreaterThan, "%s")
    print(inner1.getCondition())

def TestConditionSetMany():
    inner1 = ConditionSet(LogicalOperators.And)
    inner1.addCondition("age", ConditionalOperators.LessThan, 0)
    inner1.addCondition("length", ConditionalOperators.GreaterThan, 3)
    assert inner1.getCondition() == "(age < 0 AND length > 3)"

    inner2 = ConditionSet(LogicalOperators.And)
    inner2.addCondition("height", ConditionalOperators.LessThan, 0, "contact")
    inner2.addCondition("weight", ConditionalOperators.GreaterThan, 3)
    assert inner2.getCondition() == "(contact.height < 0 AND weight > 3)"

    outer = ConditionSet(LogicalOperators.Or)
    outer.addConditionSet(inner1)
    outer.addConditionSet(inner2)
    outer.addCondition("name", ConditionalOperators.NotNull)
    outer.addCondition("emailAddress", ConditionalOperators.NotEqual, "Leo@Gmail.com", "contact")
    assert outer.getCondition() == "(name IS NOT NULL OR contact.emailAddress != Leo@Gmail.com OR (age < 0 AND length > 3) OR (contact.height < 0 AND weight > 3))"

    q = Query("contact")
    q.addSingleCondition("county", ConditionalOperators.Equal, "Hennepin")
    q.addConditionSet(outer)
    query = q.getQuery()
    print(query)
    assert query == "SELECT * FROM contact WHERE county = Hennepin OR (name IS NOT NULL OR contact.emailAddress != Leo@Gmail.com OR (age < 0 AND length > 3) OR (contact.height < 0 AND weight > 3))"


def main():
    TestNewSelectAll()
    TestSelectAttributes()
    TestSelectAttributesWithTableName()
    TestInnerJoin()
    TestInnerJoinWithAlias()
    TestAddCondition()
    TestAddConditionWithTableName()
    TestGroupBySingle()
    TestGroupByMultiple()
    TestOrderBySingleDesc()
    TestOrderByMultipleDescAndAsc()
    TestConditionSetAND()
    TestConditionSetOR()
    TestConditionSetSingle()
    TestConditionSimple()
    TestConditionSetMany()

main()