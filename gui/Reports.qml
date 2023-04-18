import QtQuick 2.3
import QtQuick.Window 2.2
import QtQuick.Controls 2.3
import QtQuick.Dialogs 1.3
//import QtQuick.Layouts 1.15

Item {
    id: idSubWindow
    width: 300
    height: 300
    Rectangle {
        anchors.fill: parent
        color: "red"
    }
    //color:  "LightGrey"
    Menu {
        id: contextMenu
        cascade: true
        MenuItem { text: "Die" }
        MenuItem { text: "Date" }
        MenuItem { text: "Type 0" }
        MenuItem { text: "Type 1" }
    }


    Rectangle {
        //id: mainRect
        // Layout.alignment:Qt.AlignHCenter

        anchors.centerIn: parent
        color: "LightGrey"
        width: 200
        height: 200

        Column {
            id: buttonColumn1
            spacing: 100
            height: implicitHeight
            width:  parent.width

            Button {
                text: "Default Report"
                anchors.horizontalCenter: parent.horizontalCenter
                //anchors.verticalCenter: parent.verticalCenter
                // onClicked: appel a la fonction generate fichier csv
            }

            Button {
                text: "Customed Report"
                anchors.horizontalCenter: parent.horizontalCenter
                //anchors.verticalCenter: parent.verticalCenter
                onClicked: {contextMenu.popup()}
            }
        }



    }
    //Text {
        //anchors.centerIn: parent
        //text: "My New Window"
    //}


}

