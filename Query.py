class ConditionalOperators:
    def __init__(self) -> None:
        pass
    
    Equal = "="
    GreaterThan = ">"
    LessThan = "<"
    Null = "IS NULL"
    NotNull = "IS NOT NULL"

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

class Orders:
    def __init__(self) -> None:
        pass

    Descending = "DESC"
    Ascending = "ASC"

class AggregateFunctions:
    def __init__(self) -> None:
        pass

    def Sum(attribute):
        return "SUM(" + str(attribute) + ")"

    def Count(attribute):
        return "COUNT(" + str(attribute) + ")"


class ConditionSet:
    def __init__(self, operator: str) -> None:
        self.operator = operator
        self.conditions = []

    def addCondition(self, attribute: str, operator: str, value: object = None, tableName: str = None):
        if tableName is not None:
            self.conditions.append({"attribute": attribute, "operator": operator, "value": str(value), "tableName": tableName})
        elif value is not None:
            self.conditions.append({"attribute": attribute, "operator": operator, "value": str(value)})
        else:
            self.conditions.append({"attribute": attribute, "operator": operator})

    def getCondition(self):
        condtionSTR = "("
        condCount = len(self.conditions)
        for condition in self.conditions:
            condCount = condCount - 1
            condtionSTR += condition["attribute"] + " " + condition["operator"]
            if "value" in condition.keys():
                condtionSTR += " " + condition["value"]    
            if condCount > 0: condtionSTR += " " + self.operator + " "
        condtionSTR += ")"
        return condtionSTR


class Query:
    
    def __init__(self, tableName):
        self.sourceTableName = tableName
        self.conditions = []
        self.joinedTables = []
        self.attributes = []
        self.orders = []
        self.groups = []
        self.orderDirection = ""

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
            self.groups.append(table + "." + attribute)
        else:
            self.groups.append(attribute)

    def addOrder(self, attribute: str, direction: str):
        self.orders.append(attribute + " " + direction)

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
                if "tableName" in condition.keys():
                    query += condition["tableName"] + "." + condition["attribute"] + " " + condition["operator"] + " " + condition["value"]
                else:
                    query += condition["attribute"] + " " + condition["operator"] + " " + condition["value"]

        if len(self.groups) > 0:
            gpCount = len(self.groups)
            query += " GROUP BY "
            for group in self.groups:
                gpCount = gpCount - 1
                query += group
                if gpCount > 0: query += ", "

        if len(self.orders) > 0:
            ordCount = len(self.orders)
            query += " ORDER BY "
            for order in self.orders:
                ordCount = ordCount - 1
                query += order
                if ordCount > 0: query += ", "
        
        query += ";"

        return query