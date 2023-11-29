from __future__ import annotations

class ConditionalOperators:
    def __init__(self) -> None:
        pass
    
    Equal = "="
    GreaterThan = ">"
    LessThan = "<"
    Null = "IS NULL"
    NotNull = "IS NOT NULL"
    NotEqual = "!="

class LogicalOperators:
    def __init__(self) -> None:
        pass

    Or = "OR"
    And = "AND"
    Not = "NOT"

class JoinOperators:

    def __init__(self) -> None:
        pass

    INNER = "INNER JOIN"
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
    # Operator here refers to a conditional operator
    def __init__(self, operator: LogicalOperators) -> None:
        self.operator = operator
        self.conditions = []
        self.conditionSets = []

    # Operator here referse to a logical operator
    def addCondition(self, attribute: str, operator: ConditionalOperators, value: object = None, tableName: str = None):
        if tableName is not None:
            self.conditions.append({"attribute": attribute, "operator": operator, "value": str(value), "tableName": tableName})
        elif value is not None:
            self.conditions.append({"attribute": attribute, "operator": operator, "value": str(value)})
        else:
            self.conditions.append({"attribute": attribute, "operator": operator})

    def addConditionSet(self, conditionSet: ConditionSet):
        self.conditionSets.append(conditionSet.getCondition())

    def getOperator(self):
        return self.operator

    def getCondition(self):
        condtionSTR = "("
        condCount = len(self.conditions)
        for condition in self.conditions:
            condCount = condCount - 1
            if "tableName" in condition.keys():
                condtionSTR += condition["tableName"] + "." +condition["attribute"] + " " + condition["operator"]
            else:
                condtionSTR += condition["attribute"] + " " + condition["operator"]
            if "value" in condition.keys():
                condtionSTR += " " + condition["value"]    
            if (condCount > 0) or (len(self.conditionSets) > 0): condtionSTR += " " + self.operator + " "
        

        condCount = len(self.conditionSets)
        for conditionSet in self.conditionSets:
            condCount = condCount - 1
            condtionSTR += conditionSet
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
        self.conditionSets = []
        self.values = []

    def Select(self, attribute: str, tableName: str = None):
        self.attributes.append({"attribute": attribute, "table": tableName})

    # Operator here refers to a logical operator
    def addSingleCondition(self, attribute: str, operator: LogicalOperators, value: object, tableName: str = None):
        if tableName is not None:
            self.conditions.append({"attribute": attribute, "operator": operator, "value": str(value), "tableName": tableName})
        else:
            self.conditions.append({"attribute": attribute, "operator": operator, "value": str(value)})

    def addConditionSet(self, conditionSet: ConditionSet):
        self.conditionSets.append(conditionSet)

    def Join(self, targetTableName: str, operator: JoinOperators, sourceProperty: str, targetProperty: str, targetAlias: str = None):
        if targetAlias is not None:
            self.joinedTables.append(operator + " " + targetTableName + " AS " + targetAlias + " ON " + self.sourceTableName + "." + sourceProperty + " = " + targetAlias + "." + targetProperty)
        else:
            self.joinedTables.append(operator + " " + targetTableName + " ON " + self.sourceTableName + "." + sourceProperty + " = " + targetProperty)

    def GroupBy(self, attribute: str, table: str = None):
        if table is not None:
            self.groups.append(table + "." + attribute)
        else:
            self.groups.append(attribute)

    def OrderBy(self, attribute: str, direction: str):
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

        if len(self.conditions) > 0 or len(self.conditionSets) > 0:
            query += " WHERE "
        
            if len(self.conditions) > 0:
                for condition in self.conditions:
                    if "tableName" in condition.keys():
                        query += condition["tableName"] + "." + condition["attribute"] + " " + condition["operator"] + " " + condition["value"]
                    else:
                        query += condition["attribute"] + " " + condition["operator"] + " " + condition["value"]

            if len(self.conditionSets) > 0:
                condSetCount = len(self.conditionSets) 
                if len(self.conditions) > 0:
                    query += " " + self.conditionSets[0].getOperator() + " "
                for conditionSet in self.conditionSets:
                    condSetCount = condSetCount - 1
                    if condSetCount > 0:
                        query += conditionSet.getOperator()    
                    query += conditionSet.getCondition()

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


        return query