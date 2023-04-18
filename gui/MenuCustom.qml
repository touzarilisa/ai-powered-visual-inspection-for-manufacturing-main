import QtQuick 2.0
import QtQuick.Window 2.2
//import QtQuick.Controls 2.0
import QtQuick.Controls 2.3
import QtQuick.Dialogs 1.2
import QtPositioning 5.5
import QtLocation 5.6

////


//import QtQuick 2.2
//import QtQuick.Controls 1.2
//import QtQuick.Dialogs 1.1
import QtQuick.Layouts 1.1
//import QtQuick.Window 2.0




Item {
    id: idRoot
    width: 1200
    height: 720
    SystemPalette { id: palette }

    // true: load the image, false: Unload it
    property bool bLoadResult: false
    property var  labelLocal: ""
    property int  xLocal: 0
    property int  yLocal: 0
    property int  widthLocal: 0
    property int  heightLocal: 0
    property bool bLoadReport: false

    property var  bLocalPath: ""




    FileDialog {
        id: idfileDialog
        title: "Choose "
        folder: shortcuts.pictures
        nameFilters: [ "Image files (*.png *.jpeg *.jpg *.gif)" ]
        selectedNameFilter: "All files (*)"
        onAccepted: {
            var path = idfileDialog.fileUrl.toString();
        
            idMyImage_drop.source = Qt.resolvedUrl(path)
            var index = path.lastIndexOf("/") + 1;
            var filename = path.substr(index);
            //idMyText.text = filename
            QmlConnector.load_image(path)
            idMyImage_drop.source = Qt.resolvedUrl(path)
            idMyRectangle_drop.width = 0
            idMyRectangle_drop.height = 0
            idMyRectangle_drop.x = 0
            idMyRectangle_drop.y = 0
            idDie.text = ""
            idIML.text = ""
            idName.text = ""
            idInspection.text = ""
            idConfidence.text = ""


        }
        onRejected: { console.log("Rejected") }
    }

    /*Column {
        id: idMyImageContainer
        width: 700
        height: 700
        x: 350
        y: 100
        opacity: 0
        spacing: 15
        Text {
            id: idMyText
            font.pixelSize: 20
            color: "white"
            style: Text.Raised
            text: ""
        }
        Image {
            id: idMyImage
            width: 500
            height: 500
            source: ""
        }
       
    }*/

  


    /*Rectangle {
        id: bottomBar
        height: buttonRow.height * 1.2
        color: Qt.darker(palette.window, 1.1)
        border.color: Qt.darker(palette.window, 1.3)
        Row {
            id: buttonRow
            spacing: 6
            anchors.left: parent.left
            anchors.leftMargin: 12
            height: implicitHeight
            width: parent.width
            Button {
                text: "Menu"
                anchors.verticalCenter: parent.verticalCenter
                onClicked: {contextMenu.popup()}
            }
           
            Button {
                text: "Display Image"
                onClicked: {
                    //si on clique une fois we load the image
                    // si on clique deux fois we Unload the image
                    bLoad = !bLoad
                }
            }
        }
    }*/

    

    ////////////////////////////////////////////////////////////////////////////////////////
    // this row will hold the buttons, to upload directly from dektop, and to generate reports
    ////////////////////////////////////////////////////////////////////////////////////////
   Item {
       id: idFirstItem
       x: 180
       y: 80
        width: 1200
        height: 300
        
            //Icon Upload
            Rectangle {
                x: 100
                width: 100
                height: 100
                color:  "#b8e0e7"
                radius: 100
            Image {
                id: idUploadImage
                width: 50
                height: 50
                anchors.centerIn: parent
                source: "ICONS/upload.png"
                
            }
            MouseArea {
                    anchors.fill: parent
                    hoverEnabled: true
                     property bool hovered: false
                    onEntered:  {
                    
                        hovered = true
                        parent.opacity = 0.5
                    }
                    onExited: parent.opacity = 1
                    onClicked: { 
                         bLoadResult = false
                        idfileDialog.open()
                  
                       
                    }
                }
        }

            Text {
                x: 110
                y: 105
                text: "Upload"
                font.pixelSize: 22
            }

             //Icon send
            Rectangle {
                x: 250
                width: 100
                height: 100
                color:  "#b8e0e7"
                radius: 100
            Image {
                id: idSendImage
                width: 50
                height: 50
                anchors.centerIn: parent
                source: "ICONS/send.png"
                
            }
            MouseArea {
                id: idMouseAreaSend
                    anchors.fill: parent
                    hoverEnabled: true
                     property bool hovered: false
                    onEntered:  {
                       
                        hovered = true
                        parent.opacity = 0.5
                    }
                    onExited: parent.opacity = 1
                   
                    onClicked: {
                        idAnimateProgressBar.start() 
                        var data = QmlConnector.send_image()
                        
                        idMyRectangle_drop.width = data[5]
                        idMyRectangle_drop.height = data[6]
                        idMyRectangle_drop.x = data[3]
                        idMyRectangle_drop.y = data[4]
                        idName.text = data[0].split(".")[0]
                        idInspection.text = data[1]
                        idConfidence.text = data[2]
                        idIML.text = data[0].split("_")[3]
                        idDie.text = data[0].split("_")[4]
                    }
                }
        }
            
            
            Text {
                x: 225
                y: 105
                text: "Send To Server"
                font.pixelSize: 22
            }

        //Classify 
           Rectangle {
                x: 400
                width: 100
                height: 100
                color:  "#b8e0e7"
                radius: 100
            Image {
                id: idClassify
                width: 50
                height: 50
                anchors.centerIn: parent
                source: "ICONS/inspect.png"
                
            }
            MouseArea {
                    anchors.fill: parent
                    hoverEnabled: true
                     property bool hovered: false
                    onEntered:  {
                        
                        hovered = true
                        parent.opacity = 0.5
                    }
                    onExited: parent.opacity = 1
                    onClicked: { 
                        bLoadResult = true

                    }
                }
        }
           
            Text {
                x: 408
                y: 105
                text: "Inspect"
                font.pixelSize: 22
            }
    
        
    //section generate reports
     
             Rectangle{
                x: 550
                width: 100
                height: 100
                color:  "#b8e0e7"
                radius: 100
            Image {
                id: idGenerateReports
                width: 50
                height: 50
                anchors.centerIn: parent
                source: "ICONS/Download.png"
                
            }
             MouseArea {
                    anchors.fill: parent
                    hoverEnabled: true
                     property bool hovered: false
                    onEntered:  {
                        
                        hovered = true
                        parent.opacity = 0.5
                    }
                    onExited: parent.opacity = 1
                    onClicked: { 
                        //bLoadReport = true
                        var component = Qt.createComponent("sub_window.qml")
                        var window    = component.createObject()
                        window.show()
                    }
                }
        }
       
            Text {
                x: 507
                y: 105
                text: "Download Report"
                font.pixelSize: 22
            }

           

       }
       //////////////////////////////End buttons////////////////////////////////////
   
    ////////////////////////////////////////////////////////////////////////////////
    // this row will be responisble for visualsing the image uploaded, and predicted
    ////////////////////////////////////////////////////////////////////////////////
    Row {
        id: idSecondRow
        x: 150
        y: 300
        spacing: 10
        //First Item: Region: display the image
    Item {
        width: 300
        height: 300
         Rectangle {
            anchors.fill: parent
            color: "#B6D5DA"
            radius: 50
         }
        
        
        Image {
                id: idDragAndDrop
                width: 50
                height: 50
                anchors.centerIn: parent
                source: "ICONS/drag_and_drop.png"
            }

            Text {
                x: 80
                y: 170
                text: "Drag and drop image"
                font.pixelSize: 16
        }
       
        // Instanciate DropArea
        DropArea {
            id: dropArea
            anchors.fill: parent
            
            onDropped: {
                bLoadResult = false
                var path = drop.text
                
                QmlConnector.load_image(path)

                //todo replace
                //idMyImage_drop.source =  path.slice(0,-2)
               idMyImage_drop.source =  path
               

                idMyRectangle_drop.width = 0
                idMyRectangle_drop.height = 0
                idMyRectangle_drop.x = 0
                idMyRectangle_drop.y = 0
                idDie.text = ""
                idIML.text = ""
                idName.text = ""
                idInspection.text = ""
                idConfidence.text = ""
            }
            onEntered: {
                
            }
            onExited: {
                
            }
        }

        Image {
            id: idMyImage_drop
            width: 224
            height: 224
            source: ""
            anchors.centerIn: parent
            opacity: 0
            Rectangle {
                id: idMyRectangle_drop
                width: 0
                height: 0
                color: "transparent"
                visible: bLoadResult
                border.color: "red"
                border.width: 3

            }
            //we should reset the opacity to 0à un moment donné , A voir 
            onSourceChanged: {
                idAnimateImage.running = true
            }
        }
    }

        NumberAnimation {
            id: idAnimateImage
            running: false
            target: idMyImage_drop
            property: "opacity"
            from: 0
            to: 1
            duration: 500
            easing.type: Easing.OutQuad
        }

    
    //section resultats: second item from a row 
    Item {
        width: 600
        height: 300
        //
        Rectangle {
            anchors.fill: parent
            color: "#B6D5DA"
            radius: 50
        } 
        Text {
            x: 200
            text: "Inspection Results"
            font.pixelSize: 22
        }
        
            Row {
                x: 20
                width: 600
                y: 50
                Text {
                    text: "Name : "
                    font.pixelSize: 16
                    }
                Text {
                    id: idName
                    text: ""
                    visible: bLoadResult
            
                }
            }
        
        
        

            Row {
                x: 20
                y: 100
                width: parent.width
                Text {
                    text: "Decision : "
                    font.pixelSize: 16
                    }
                Text {
                    id: idInspection
                    text: ""
                    color: (idInspection.text == "Defected") ? "red": "green"
                    visible: bLoadResult

                }
            }
        
        
            Row {
                x: 20
                y: 150
                width: parent.width
                Text {
                    text: "IML : "
                    font.pixelSize: 16
                    }
                Text {
                    id: idIML
                    text: ""
                    visible: bLoadResult
                }
            }
        
        
            Row {
                x: 20
                y: 200
                width: parent.width
                Text {
                    text: "Die: "
                    font.pixelSize: 16
                    }
                Text {
                    id: idDie
                    text: ""
                    visible: bLoadResult

                }
            }
        
        
        
            Row {
                x: 20
                y: 250
                width: parent.width
                Text {
                    text: "Confidence of inspection : "
                    font.pixelSize: 16
                    }
                Text {
                    id: idConfidence
                    text: ""
                    visible: bLoadResult
                }
                Text {
                    id: idPerce
                    text: "%"
                    visible: bLoadResult
                }

            }
        

        
    }

    }
    

    

  
   
    //////////////////////////////////////////////////////////////////////////////
    //connection with the QmlConnector Component and catch the signals sent from Py
    //////////////////////////////////////////////////////////////////////////////
     


     


 


    



Rectangle {
    id: idPb
    x: 300
    y: 620
    width: 600
    height: 50
    radius: height / 2
    color: "white"
    property int percentage: 0


    Item {
        id: cliprect
        anchors.bottom: parent.bottom
        anchors.top: parent.top
        anchors.left: parent.left
        width: parent.width * parent.percentage / 100
        clip: true

        Rectangle {
            width: idPb.width                        
            height: idPb.height 
            radius: height / 2
            anchors.bottom: parent.bottom
            anchors.left: parent.left
            color: "#b8e0e7"
        }
    }
}

    SequentialAnimation{
        id: idAnimateProgressBar
        NumberAnimation {
            target: idPb
            property: "percentage"
            from: 0
            to: 100
            duration: 3000
            running: false
            alwaysRunToEnd: true
            easing.type: Easing.OutQuart
            }
            
        ScriptAction{
            script: {
                
                idPb.percentage = 0
            }
        }

    }

/*idAnimateProgressBar.o: {
    console.log("idAnimateProgressBar.onFinished")
    idPb.percentage = 0
}*/
        

   

}

