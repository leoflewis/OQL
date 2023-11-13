class ConditionalOperators:
    def __init__(self) -> None:
        pass
    
    Equal = "="
    GreaterThan = ">"
    LessThan = "<"


class LogicalOperators:
    def __init__(self) -> None:
        pass

    Or = "OR"
    And = "AND"
    Not = "NOT"

class JoinOperators:

    def __init__(self) -> None:
        pass

    Inner = "INNER JOIN"
    Left = "LEFT OUTER JOIN"
    Right = "RIGHT OUTER JOIN"

class Query:
    
    def __init__(self, tableName):
        self.sourceTableName = tableName
        self.conditions = []
        self.joinedTables = []
        self.attributes = []
        self.orders = []
        self.groupBy = []

    def addAttribute(self, attribute: str, tableName: str = None):
        self.attributes.append({"attribute": attribute, "table": tableName})
        

    def addCondition(self, attribute: str, operator: str, value: object, tableName: str = None):
        if tableName is not None:
            self.conditions.append({"attribute": attribute, "operator": operator, "value": str(value), "tableName": tableName})
        else:
            self.conditions.append({"attribute": attribute, "operator": operator, "value": str(value)})

    def joinTable(self, targetTableName: str, operator: str, sourceProperty: str, targetProperty: str, targetAlias: str = None):
        if targetAlias is not None:
            self.joinedTables.append(operator + " " + targetTableName + " AS " + targetAlias + " ON " + self.sourceTableName + "." + sourceProperty + " = " + targetAlias + "." + targetProperty)
        else:
            self.joinedTables.append(operator + " " + targetTableName + " ON " + self.sourceTableName + "." + sourceProperty + " = " + targetProperty)

    def addGroup(self, attribute: str, table: str = None):
        if table is not None:
            self.groupBy.append(table + "." + attribute)
        else:
            self.groupBy.append(attribute)

    def addOrder(self, attribute: str, direction: str):
        self.orders.append({"attribute": attribute, "direction": direction})

    def getQuery(self):
        query = "SELECT "
        
        if len(self.attributes) == 0:
            query += "*"
        else:
            attrCount = len(self.attributes)
            for attribute in self.attributes:
                attrCount = attrCount - 1
                if attribute["table"] is not None:
                    query += attribute["table"] + "." + attribute["attribute"] 
                else:
                    query += attribute["attribute"] 
                
                if attrCount > 0: query += ", "
        
        query += " FROM " + self.sourceTableName

        for joinTable in self.joinedTables:
            query += " " + joinTable

        if len(self.conditions) > 0:
            query += " WHERE "
            for condition in self.conditions:
                if condition["tableName"] is not None:
                    query += condition["tableName"] + "." + condition["attribute"] + " " + condition["operator"] + " " + condition["value"]
                else:
                    query += condition["attribute"] + " " + condition["operator"] + " " + condition["value"]

        if len(self.groupBy) > 0:
            query += " GROUP BY "
            for group in self.groupBy:
                query += group

        if len(self.orders) > 0:
            query += " ORDER BY "
            for order in self.orders:
                query += order
        
        query += ";"

        return query