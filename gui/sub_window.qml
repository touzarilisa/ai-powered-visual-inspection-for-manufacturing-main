import QtQuick 2.3
import QtQuick.Window 2.2
import QtQuick.Controls 2.3
import QtQuick.Dialogs 1.3
import QtQuick.Controls.Styles 1.4
//import QtQuick.Layouts 1.15

Window {
    id: sub_window
    width: 400
    height: 400
    color:  "LightGrey"

    // menu of customed report
    Menu {
        id: contextMenu
        cascade: true

        MenuItem {
            //text: "Die"
            TextField {
                id: dieField
                placeholderText: qsTr("Choose Die number: 1, 2, 3, 4")
            }
            onTriggered: {

                QmlConnector.report_csv_die(dieField.text)
                QmlConnector.report_download()
                Window.window.close()
                var popupComponent  = Qt.createComponent("msg_report.qml")
                var popup2 = popupComponent.createObject(idRoot, {"parent" : idRoot});
                popup2.open()
            }

        }
        MenuSeparator { }
        MenuItem {

            TextField {
                id: dateField
                placeholderText: qsTr("Enter Year")
            }
            onTriggered: {
                QmlConnector.report_csv_date(dateField.text)
                QmlConnector.report_download()
                Window.window.close()
                var popupComponent  = Qt.createComponent("msg_report.qml")
                var popup2 = popupComponent.createObject(idRoot, {"parent" : idRoot});
                popup2.open()
            }
        }
        MenuSeparator { }
        MenuItem {
            TextField {
                id: typeField
                placeholderText: qsTr("0: Defected, 1: Not Defected")
                //onTextChanged: QmlConnector.text = text
            }
            onTriggered: {
                QmlConnector.report_csv_type(typeField.text)
                QmlConnector.report_download()
                Window.window.close()
                var popupComponent  = Qt.createComponent("msg_report.qml")
                var popup2 = popupComponent.createObject(idRoot, {"parent" : idRoot});
                popup2.open()
            }
        }
        }

    // sub_window
    Rectangle {

        anchors.centerIn: parent
        color: "LightGrey"
        width: 300
        height: 300

        Column {
            id: buttonColumn1
            spacing: 100
            height: implicitHeight
            width:  parent.width

            Button {
                text: "Default Report"
                anchors.horizontalCenter: parent.horizontalCenter                
                //appel a la fonction generate fichier csv
                onClicked:{
                    QmlConnector.report_csv()
                    QmlConnector.report_download()
                    Window.window.close()
                    var popupComponent  = Qt.createComponent("msg_report.qml")
                    var popup2 = popupComponent.createObject(idRoot, {"parent" : idRoot});
                    popup2.open()

                }
            }

            Button {
                text: "Customed Report"
                anchors.horizontalCenter: parent.horizontalCenter
                //anchors.verticalCenter: parent.verticalCenter
                onClicked: {
                    contextMenu.popup()
                }
            }
        }

    }

}


