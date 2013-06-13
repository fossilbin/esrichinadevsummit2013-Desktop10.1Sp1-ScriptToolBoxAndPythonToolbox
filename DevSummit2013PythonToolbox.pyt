import arcpy

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "mutlToolbox"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [Reclass]

class Reclass(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Reclass"
        self.description = "根据指定字段重分类，并将值写入另一个字段当中"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        fc = arcpy.Parameter(
                displayName='Input Features',
                name='in_features',
                datatype='GPTableView',
                parameterType='Required',
                direction='Input')
                
        fd = arcpy.Parameter(
                displayName='Reclass Field',
                name='reclass_field',
                datatype='Field',
                parameterType='Required',
                direction='Input')
        fd.parameterDependencies = [fc.name]
        fd.filter.list = ['Text']
        
        fd1 = arcpy.Parameter(
                displayName='Destination Field',
                name='destination_field',
                datatype='Field',
                parameterType='Required',
                direction='Input')
        fd1.parameterDependencies = [fc.name]
        fd1.filter.list = ['Text']
                
        vt = arcpy.Parameter(
                displayName='Reclass Mapping',
                name='reclass_mapping',
                datatype='GPValueTable',
                parameterType='Required',
                direction='Input')
        vt.columns = [['GPString', 'Old Value'], ['GPString', 'New Value']]

        params = [fc,fd,fd1,vt]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        tableView = parameters[0].valueAsText
        reclassFd = parameters[1].valueAsText
        inMemoryTable = 'in_memory/tempFre'
        
        if parameters[0].altered and parameters[1].altered and not parameters[1].hasBeenValidated:
            # result = arcpy.Frequency_analysis(parameters[0].value,'in_memory/tempFre',reclassFd)
            if arcpy.Exists(inMemoryTable):
                arcpy.Delete_management(inMemoryTable)
            result = arcpy.Frequency_analysis(tableView,inMemoryTable,reclassFd)
            cur = arcpy.da.SearchCursor(result.getOutput(0),reclassFd)
            temp = []
            for row in cur:
                if row[0] == None:
                    temp.append(['NULL',''])
                else:
                    temp.append([row[0],''])
            parameters[3].values = temp
            
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        tableView = parameters[0].value
        srcFd = parameters[1].valueAsText
        destiFd = parameters[2].valueAsText
        vt = parameters[-1].values
        # print tableView
        arcpy.AddMessage(tableView)
        arcpy.AddMessage(type(tableView))
        if arcpy.Exists('in_memory/tempFre'):
            arcpy.Delete_management('in_memory/tempFre')
            
        validFd = arcpy.AddFieldDelimiters(tableView,srcFd)
        for old,new in vt:
            if old == 'NULL':
                sql = validFd + ' IS NULL'
            else:
                sql = validFd + " = '{}'".format(old)
            
            arcpy.AddMessage(sql)            
            arcpy.MakeTableView_management(tableView,'tbv',sql)
            
            if new.upper() == 'NULL':
                arcpy.CalculateField_management('tbv',destiFd,'None','PYTHON_9.3') 
            else:
                arcpy.CalculateField_management('tbv',destiFd,'"{}"'.format(new))
            
        