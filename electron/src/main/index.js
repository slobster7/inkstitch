const path = require('path')
const fs = require('fs')
const tmp = require('tmp')
const url = require('url')
const { app, BrowserWindow, ipcMain, dialog, shell } = require('electron')

//moves the URL to proper position
if (process.argv.includes("http://127.0.0.1:5000/")) {
process.argv.shift()
process.argv.shift()
}

// older code that sets the url for the path I would assume
var target = process.argv[1] || ""

var targetURL = url.parse(target)
var winURL = null
// Print PDF will give us a full URL to a flask server, bypassing Vue entirely.
// Eventually this will be migrated to Vue.
if (targetURL.protocol) {
    winURL = target
} else if(!target) {
    // check if target exist, which will not in production(installed) mode.
    winURL = "http://127.0.0.1:5000/"
} else {
    winURL = `file://${__dirname}/index.html?${targetURL.query || ""}#${targetURL.pathname || ""}`
}

function createWindow() {
    const mainWindow = new BrowserWindow({
        useContentSize: true,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false,
        },
    })
    if (winURL == "http://127.0.0.1:5000/" && target) {
        mainWindow.loadURL(winURL)
        mainWindow.webContents.openDevTools()
    } else {
        mainWindow.loadURL(winURL)
    }
    mainWindow.maximize()
    // ipc doesn't work with the updated version of electron. 
    ipcMain.on('save-pdf', function (event, pageSize) {
        mainWindow.webContents.printToPDF({"pageSize": pageSize}, function(error, data) {
            dialog.showSaveDialog(mainWindow, {"defaultPath": "inkstitch.pdf"}, function(filename, bookmark) {
                if (typeof filename !== 'undefined')
                    fs.writeFileSync(filename, data, 'utf-8');
            })
        })
    })
    // an issue with tmp may occuer
    ipcMain.on('open-pdf', function (event, pageSize) {
        mainWindow.webContents.printToPDF({"pageSize": pageSize}, function(error, data) {
            tmp.file({keep: true, discardDescriptor: true}, function(err, path, fd, cleanupCallback) {
                fs.writeFileSync(path, data, 'utf-8');
                shell.openItem(path);
            })
        })
    })
}

app.whenReady().then(() => {
    createWindow()
    
    app.on('activate', () => {
        if(BrowserWindow.getAllWindows().length === 0)  {
            createWindow()
        }
    })
})

app.on('window-all-closed', () => {
    app.quit()
})

