import QtQuick 2.3
import QtQuick.Window 2.2
import QtQuick.Controls 2.3
import QtQuick.Dialogs 1.3
import QtQuick.Controls.Styles 1.4
//import QtQuick.Layouts 1.15

Popup {
    x: 500
    y: 300
    width: 260
    height: 40
    modal: true
    focus: true
    closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside
    visible: false

    Text {
        text:  "Find report in Downloads Directory"
    }
}




