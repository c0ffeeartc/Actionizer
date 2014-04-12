import json


def getBuiltinStep(Uid):
    for step in builtinSteps:
        if step["Uid"] == Uid:
            return step
    print ("No such builtin step")
    return builtinSteps[0]

# Step list
builtinSteps = [{
                    "typename": "step",
                    "Uid": "nullStep",
                    "arguments": [None], # None
                    "preRequisites": [None],
                    "script": "alert ('nullStep');"
                }, {
                    "typename": "step",
                    "Uid": "newLayer",
                    "arguments": [False], # below
                    "argNames": ["below"],
                    "argTypenames": ["bool"],
                    "preRequisites": ["activeLayer", "activeDocument"],
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
                }, {
                    "typename": "step",
                    "Uid": "helloResult",
                    "returns": True, # returns value
                    "arguments": [
                        [None, None, None]  # [argValue, argTypename, argName]
                    ],
                    "result": [
                        ["Hello, Result!", "string", "result"],
                        [4, "number", "result2"],
                    ],
                    "preRequisites": ["activeLayer", "activeDocument"],
                    "script": """
        result[1][1] = 102;
        alert(result);
    """
                }, {
                    "typename": "step",
                    "Uid": "renameLayer",
                    "arguments": [None], # name
                    "argNames": ["name"],
                    "argTypenames": ["string"],
                    "preRequisites": ["activeLayer", "activeDocument"],
                    "script": """
if (arguments[0]){
    newName = arguments[0];
    activeDocument.activeLayer.name = newName;
}
    """
                }, {
                    "typename": "step",
                    "Uid": "selectNextLayer",
                    "arguments": [False], # makeVisible:boolean
                    "preRequisites": ["activeLayer", "activeDocument"],
                    "script": """
    makeVisible = arguments[0]

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
                }, {
                    "typename": "step",
                    "Uid": "selectPreviousLayer",
                    "arguments": [False], # makeVisible:boolean  # does nothing
                    "preRequisites": ["activeLayer", "activeDocument"],
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
                }, {
                    "typename": "step",
                    "Uid": "bringForward",
                    "arguments": [None], # None
                    "preRequisites": ["activeLayer", "activeDocument"],
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
                    "typename": "step",
                    "Uid": "bringToFront",
                    "arguments": [None], # None
                    "preRequisites": ["activeLayer", "activeDocument"],
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
                }, {
                    "typename": "step",
                    "Uid": "sendBackward",
                    "arguments": [None],
                    "preRequisites": ["activeLayer", "activeDocument"],
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
                }, {
                    "typename": "step",
                    "Uid": "sendToBack",
                    "arguments": [None], # None
                    "preRequisites": ["activeLayer", "activeDocument"],
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
                }, {
                    "typename": "step",
                    "Uid": "deleteActiveLayer",
                    "arguments": [None], # None
                    "preRequisites": ["activeLayer", "activeDocument"],
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
                    "typename": "step",
                    "Uid": "activateLayerByIndex",
                    "arguments": [0], # index
                    "argNames": ["index"],
                    "preRequisites": ["activeDocument"],
                    "script": """
    argLayerIndex = arguments[0]
    activeDocument.activeLayer=activeDocument.layers[argLayerIndex];
"""
                },
]

if __name__ == "__main__":
    with open("builtinSteps.json", mode='w') as f:
        builtinStepsJson = json.dump(builtinSteps, f)
