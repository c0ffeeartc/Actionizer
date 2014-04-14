import json


def get_builtin_step(uid):
    for step in builtinSteps:
        if step["uid"] == uid:
            return step
    print("No such builtin step")
    return builtinSteps[0]

# Step list
builtinSteps = [
    {
        "type_name": "step",
        "uid": "nullStep",
        "argument_collection": [None],  # None
        "pre_conditions": [None],
        "script": "alert ('nullStep');"
    },
    {
        "type_name": "step",
        "uid": "testStep",
        "argNames": ["someName"],
        "argValues": ["someValue"],
        "argTypes": ["string"],
        "argument_collection": ["asdf", "string", "someName"],  # None
        "pre_conditions": [None],
        "script": "alert ('testStep');alert(arguments[0]);"
    },
    {
        "type_name": "step",
        "uid": "newLayer",
        "argument_collection": [
            [False, "bool", "below"]  # [argValue, argtype_name, argName]
        ],
        "pre_conditions": ["activeLayer", "activeDocument"],
        "script": """
        var idMk = charIDToTypeID( "Mk  " );
            var desc5 = new ActionDescriptor();
            var idnull = charIDToTypeID( "null" );
                var ref3 = new ActionReference();
                var idLyr = charIDToTypeID( "Lyr " );
                ref3.putClass( idLyr );
            desc5.putReference( idnull, ref3 );
            var idbelow = stringIDToTypeID( "below" );
            desc5.putBoolean( idbelow, args.argValues[0] );
        executeAction( idMk, desc5, DialogModes.NO );"""
    },
    {
        "type_name": "step",
        "uid": "helloResult",
        "hasReturn": True,  # hasReturn value
        "argument_collection": [
            [None, None, None]  # [argValue, argtype_name, argName]
        ],
        "result": [
            ["Hello, Result!", "string", "result"],
            [4, "number", "result2"],
        ],
        "pre_conditions": ["activeLayer", "activeDocument"],
        "script": """
        result[1][1] = 102;
        alert(result);
    """
    },
    {
        "type_name": "step",
        "uid": "renameLayer",
        "argument_collection": [None],  # name
        "argNames": ["name"],
        "argtype_names": ["string"],
        "pre_conditions": ["activeLayer", "activeDocument"],
        "script": """
if (arguments[0]){
    newName = arguments[0];
    activeDocument.activeLayer.name = newName;
}
    """
    },
    {
        "type_name": "step",
        "uid": "selectNextLayer",
        "argument_collection": [False],  # makeVisible:boolean
        "pre_conditions": ["activeLayer", "activeDocument"],
        "script": """
    makeVisible = argument_collection[0]

var idslct = charIDToTypeID( "slct" );
    var desc13 = new ActionDescriptor();
    var idnull = charIDToTypeID( "null" );
        var ref15 = new ActionReference();
        var idLyr = charIDToTypeID( "Lyr " );
        var idOrdn = charIDToTypeID( "Ordn" );
        var idFrwr = charIDToTypeID( "Frwr" );
        ref15.putEnumerated( idLyr, idOrdn, idFrwr );
    desc13.putReference( idnull, ref15 );
    var idMkVs = charIDToTypeID( "MkVs" );
    desc13.putBoolean( idMkVs, makeVisible );
executeAction( idslct, desc13, DialogModes.NO );"""
    },
    {
        "type_name": "step",
        "uid": "selectPreviousLayer",
        "argument_collection": [False],  # makeVisible:boolean  # does nothing
        "pre_conditions": ["activeLayer", "activeDocument"],
        "script": """
    makeVisible = arguments[0]

var idslct = charIDToTypeID( "slct" );
    var desc12 = new ActionDescriptor();
    var idnull = charIDToTypeID( "null" );
        var ref14 = new ActionReference();
        var idLyr = charIDToTypeID( "Lyr " );
        var idOrdn = charIDToTypeID( "Ordn" );
        var idBckw = charIDToTypeID( "Bckw" );
        ref14.putEnumerated( idLyr, idOrdn, idBckw );
    desc12.putReference( idnull, ref14 );
    var idMkVs = charIDToTypeID( "MkVs" );
    desc12.putBoolean( idMkVs, false );
executeAction( idslct, desc12, DialogModes.NO );"""
    },
    {
        "type_name": "step",
        "uid": "bringForward",
        "argument_collection": [None],  # None
        "pre_conditions": ["activeLayer", "activeDocument"],
        "script": """
var idmove = charIDToTypeID( "move" );
    var desc10 = new ActionDescriptor();
    var idnull = charIDToTypeID( "null" );
        var ref10 = new ActionReference();
        var idLyr = charIDToTypeID( "Lyr " );
        var idOrdn = charIDToTypeID( "Ordn" );
        var idTrgt = charIDToTypeID( "Trgt" );
        ref10.putEnumerated( idLyr, idOrdn, idTrgt );
    desc10.putReference( idnull, ref10 );
    var idT = charIDToTypeID( "T   " );
        var ref11 = new ActionReference();
        var idLyr = charIDToTypeID( "Lyr " );
        var idOrdn = charIDToTypeID( "Ordn" );
        var idNxt = charIDToTypeID( "Nxt " );
        ref11.putEnumerated( idLyr, idOrdn, idNxt );
    desc10.putReference( idT, ref11 );
executeAction( idmove, desc10, DialogModes.NO );"""
    }, {
        "type_name": "step",
        "uid": "bringToFront",
        "argument_collection": [None],  # None
        "pre_conditions": ["activeLayer", "activeDocument"],
        "script": """
var idmove = charIDToTypeID( "move" );
    var desc11 = new ActionDescriptor();
    var idnull = charIDToTypeID( "null" );
        var ref12 = new ActionReference();
        var idLyr = charIDToTypeID( "Lyr " );
        var idOrdn = charIDToTypeID( "Ordn" );
        var idTrgt = charIDToTypeID( "Trgt" );
        ref12.putEnumerated( idLyr, idOrdn, idTrgt );
    desc11.putReference( idnull, ref12 );
    var idT = charIDToTypeID( "T   " );
        var ref13 = new ActionReference();
        var idLyr = charIDToTypeID( "Lyr " );
        var idOrdn = charIDToTypeID( "Ordn" );
        var idFrnt = charIDToTypeID( "Frnt" );
        ref13.putEnumerated( idLyr, idOrdn, idFrnt );
    desc11.putReference( idT, ref13 );
executeAction( idmove, desc11, DialogModes.NO );
"""
    },
    {
        "type_name": "step",
        "uid": "sendBackward",
        "argument_collection": [None],
        "pre_conditions": ["activeLayer", "activeDocument"],
        "script": """
var idmove = charIDToTypeID( "move" );
    var desc8 = new ActionDescriptor();
    var idnull = charIDToTypeID( "null" );
        var ref6 = new ActionReference();
        var idLyr = charIDToTypeID( "Lyr " );
        var idOrdn = charIDToTypeID( "Ordn" );
        var idTrgt = charIDToTypeID( "Trgt" );
        ref6.putEnumerated( idLyr, idOrdn, idTrgt );
    desc8.putReference( idnull, ref6 );
    var idT = charIDToTypeID( "T   " );
        var ref7 = new ActionReference();
        var idLyr = charIDToTypeID( "Lyr " );
        var idOrdn = charIDToTypeID( "Ordn" );
        var idPrvs = charIDToTypeID( "Prvs" );
        ref7.putEnumerated( idLyr, idOrdn, idPrvs );
    desc8.putReference( idT, ref7 );
executeAction( idmove, desc8, DialogModes.NO );
"""
    },
    {
        "type_name": "step",
        "uid": "sendToBack",
        "argument_collection": [None],  # None
        "pre_conditions": ["activeLayer", "activeDocument"],
        "script": """
var idmove = charIDToTypeID( "move" );
    var desc9 = new ActionDescriptor();
    var idnull = charIDToTypeID( "null" );
        var ref8 = new ActionReference();
        var idLyr = charIDToTypeID( "Lyr " );
        var idOrdn = charIDToTypeID( "Ordn" );
        var idTrgt = charIDToTypeID( "Trgt" );
        ref8.putEnumerated( idLyr, idOrdn, idTrgt );
    desc9.putReference( idnull, ref8 );
    var idT = charIDToTypeID( "T   " );
        var ref9 = new ActionReference();
        var idLyr = charIDToTypeID( "Lyr " );
        var idOrdn = charIDToTypeID( "Ordn" );
        var idBack = charIDToTypeID( "Back" );
        ref9.putEnumerated( idLyr, idOrdn, idBack );
    desc9.putReference( idT, ref9 );
executeAction( idmove, desc9, DialogModes.NO );"""
    },
    {
        "type_name": "step",
        "uid": "deleteActiveLayer",
        "argument_collection": [None],  # None
        "pre_conditions": ["activeLayer", "activeDocument"],
        "script": """
var idDlt = charIDToTypeID( "Dlt " );
    var desc5 = new ActionDescriptor();
    var idnull = charIDToTypeID( "null" );
        var ref4 = new ActionReference();
        var idLyr = charIDToTypeID( "Lyr " );
        var idOrdn = charIDToTypeID( "Ordn" );
        var idTrgt = charIDToTypeID( "Trgt" );
        ref4.putEnumerated( idLyr, idOrdn, idTrgt );
    desc5.putReference( idnull, ref4 );
executeAction( idDlt, desc5, DialogModes.NO );"""
    }, {
        "type_name": "step",
        "uid": "activateLayerByIndex",
        "argument_collection": [0],  # index
        "argNames": ["index"],
        "pre_conditions": ["activeDocument"],
        "script": """
    argLayerIndex = arguments[0]
    activeDocument.activeLayer=activeDocument.layers[argLayerIndex];
"""
    },
]

if __name__ == "__main__":
    with open("builtinSteps.json", mode='w') as f:
        builtinStepsJson = json.dump(builtinSteps, f)
