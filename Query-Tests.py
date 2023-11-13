from Query import *

def TestNewSelectAll():
    q = Query("contact")
    query = q.getQuery()
    exQuery = "SELECT * FROM contact;"
    assert query == exQuery

def TestSelectAttributes():
    q = Query("contact")
    q.addAttribute("firstName")
    q.addAttribute("lastName")
    query = q.getQuery()
    exQuery = "SELECT firstName, lastName FROM contact;"
    assert query == exQuery

def TestSelectAttributesWithTableName():
    q = Query("contact")
    q.addAttribute("firstName", "contact")
    q.addAttribute("lastName", "contact")
    query = q.getQuery()
    exQuery = "SELECT contact.firstName, contact.lastName FROM contact;"
    assert query == exQuery

def TestInnerJoin():
    q = Query("contact")
    q.joinTable("account", JoinOperators.Inner, "contactid", "contactid")
    query = q.getQuery()
    exQuery = "SELECT * FROM contact INNER JOIN account ON contact.contactid = contactid;"
    assert query == exQuery

def TestInnerJoinWithAlias():
    q2 = Query("contact")
    q2.joinTable("account", JoinOperators.Inner, "contactid", "contactid", "acc")
    query = q2.getQuery()
    exQuery = "SELECT * FROM contact INNER JOIN account AS acc ON contact.contactid = acc.contactid;"
    assert query == exQuery

def TestAddCondition():
    q = Query("contact")
    q.addCondition("age", ConditionalOperators.GreaterThan, 50)
    query = q.getQuery()
    exQuery = "SELECT * FROM contact WHERE age > 50;"
    assert query == exQuery

def TestAddConditionWithTableName():
    q = Query("contact")
    q.addCondition("age", ConditionalOperators.GreaterThan, 50, "contact")
    query = q.getQuery()
    exQuery = "SELECT * FROM contact WHERE contact.age > 50;"
    assert query == exQuery

def TestGroupBySingle():
    q = Query("contact")
    q.addAttribute("lastName")
    q.addAttribute(AggregateFunctions.Count("id"))
    q.addGroup("lastName")
    query = q.getQuery()
    exQuery = "SELECT lastName, COUNT(id) FROM contact GROUP BY lastName;"
    assert query == exQuery

def TestGroupByMultiple():
    q = Query("contact")
    q.addAttribute("lastName")
    q.addAttribute("firstName")
    q.addAttribute(AggregateFunctions.Count("id"))
    q.addGroup("lastName")
    q.addGroup("firstName")
    query = q.getQuery()
    exQuery = "SELECT lastName, firstName, COUNT(id) FROM contact GROUP BY lastName, firstName;"
    assert query == exQuery

def TestOrderBySingleDesc():
    q = Query("contact")
    q.addOrder("lastName", Orders.Descending)
    query = q.getQuery()
    exQuery = "SELECT * FROM contact ORDER BY lastName DESC;"
    assert query == exQuery

def TestOrderByMultipleDescAndAsc():
    q = Query("contact")
    q.addOrder("lastName", Orders.Descending)
    q.addOrder("firstName", Orders.Ascending)
    query = q.getQuery()
    exQuery = "SELECT * FROM contact ORDER BY lastName DESC, firstName ASC;"
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

main()