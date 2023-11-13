from Query import Query, LogicalOperators, JoinOperators, ConditionalOperators



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
    q.addAttribute("firstName")
    q.addAttribute("lastName")
    query = q.getQuery()
    exQuery = "SELECT firstName, lastName FROM contact;"
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
    q.addCondition("age", ConditionalOperators.GreaterThan, 50, "contact")
    query = q.getQuery()
    print(query)

def main():
    TestNewSelectAll()
    TestSelectAttributes()
    TestInnerJoin()
    TestInnerJoinWithAlias()
    TestAddCondition()

main()