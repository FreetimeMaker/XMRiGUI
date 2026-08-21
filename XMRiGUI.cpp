#include "XMRiGUI.h"
#include <QApplication>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QGridLayout>
#include <QFrame>
#include <QJsonDocument>
#include <QJsonObject>
#include <QFile>
#include <QDir>
#include <QStandardPaths>
#include <QMessageBox>
#include <QDesktopServices>
#include <QRegularExpression>
#include <QTextCharFormat>
#include <QNetworkRequest>
#include <QCloseEvent>

XMRiGUIWindow::XMRiGUIWindow(QWidget *parent) : QMainWindow(parent) {
    cryptos = {"Bitcoin", "Litecoin", "Ethereum Classic", "Monero", "Ravencoin", "Uplexa", "Chukwa", "Chukwa v2", "CCX", "Keva", "Dero", "Talleo", "Safex", "ArQmA", "NINJA", "Raptoreum", "Wownero", "Scala", "Haven Protocol", "MoneroV", "Epic Cash", "Graft", "Oxen", "Stellite"};
    algos = {"sha256d", "scrypt", "etchash", "rx/0", "kawpow", "cn/upx2", "argon2/chukwa", "argon2/chukwav2", "cn/ccx", "rx/keva", "astrobwt", "cn-pico/tlo", "rx/sfx", "rx/arq", "argon2/ninja", "gr", "rx/wow", "panthera", "cn-heavy/xhv", "rx/v", "rx/epic", "rx/graft", "rx/loki", "rx/xtl"};

    loadPaths();
    loadConfig();
    setupUI();
    setupTray();

    networkManager = new QNetworkAccessManager(this);
    connect(networkManager, &QNetworkAccessManager::finished, this, &XMRiGUIWindow::onUpdateCheckFinished);

    checkAppUpdates();
    checkMinerUpdates();

    setWindowTitle("XMRiGUI " + APP_VERSION);
    setMinimumSize(900, 800);
}

XMRiGUIWindow::~XMRiGUIWindow() {
    for (auto* proc : processes) {
        if (proc->state() != QProcess::NotRunning) {
            proc->terminate();
            proc->waitForFinished(2000);
        }
    }
}

void XMRiGUIWindow::loadPaths() {
    QString appDir = qApp->applicationDirPath();

    // Basispfade zu deinen Binär-Ordnern
    QString winAssets = "C:/Users/jamie/OneDrive/Documentos/datasaver/Git/XMRiGUI Windows";
    QString linAssets = "C:/Users/jamie/OneDrive/Documentos/datasaver/Git/XMRiGUI";

#ifdef Q_OS_WIN
    settingsPath = QStandardPaths::writableLocation(QStandardPaths::AppDataLocation) + "/xmrigui.json";

    // Suche erst im Assets-Ordner, dann lokal
    if (QDir(winAssets).exists()) {
        xmrigPath = winAssets + "/xmrig.exe";
        cpuminerPath = winAssets + "/minerd.exe";
        lolminerPath = winAssets + "/lolMiner.exe";
        cudaPluginPath = winAssets + "/libxmrig-cuda.dll";
        iconPath = winAssets + "/xmrigui.png";
    } else {
        xmrigPath = appDir + "/xmrig.exe";
        cpuminerPath = appDir + "/minerd.exe";
        lolminerPath = appDir + "/lolMiner.exe";
        cudaPluginPath = appDir + "/libxmrig-cuda.dll";
        iconPath = appDir + "/xmrigui.png";
    }
#else
    settingsPath = QDir::homePath() + "/.config/xmrigui.json";

    if (QDir(linAssets).exists()) {
        xmrigPath = linAssets + "/xmrig";
        cpuminerPath = linAssets + "/minerd";
        lolminerPath = linAssets + "/lolMiner";
        cudaPluginPath = linAssets + "/libxmrig-cuda.so";
        iconPath = linAssets + "/xmrigui.png";
    } else {
        xmrigPath = "/opt/xmrigui/xmrig";
        if (!QFile::exists(xmrigPath)) xmrigPath = appDir + "/xmrig";
        cpuminerPath = appDir + "/minerd";
        lolminerPath = appDir + "/lolMiner";
        cudaPluginPath = appDir + "/libxmrig-cuda.so";
        iconPath = appDir + "/xmrigui.png";
    }
#endif
    QDir().mkpath(QFileInfo(settingsPath).absolutePath());
}

void XMRiGUIWindow::setupTray() {
    trayIcon = new QSystemTrayIcon(this);
    QIcon icon(iconPath);
    if (icon.isNull()) icon = QApplication::style()->standardIcon(QStyle::SP_ComputerIcon);
    trayIcon->setIcon(icon);

    QMenu* menu = new QMenu(this);
    menu->addAction("Show Window", this, &XMRiGUIWindow::showWindow);
    menu->addSeparator();
    for (int i = 0; i < 3; ++i) {
        QString id = QString("profile-%1").arg(i);
        QAction* act = menu->addAction(QString("Toggle Profile %1").arg(i+1));
        connect(act, &QAction::triggered, [this, id](){
            bool newState = !configs[id].mine;
            widgets[id].mineBtn->setChecked(newState);
        });
    }
    menu->addSeparator();
    menu->addAction("Quit", this, &XMRiGUIWindow::quitApp);

    trayIcon->setContextMenu(menu);
    connect(trayIcon, &QSystemTrayIcon::activated, this, &XMRiGUIWindow::trayIconActivated);
    trayIcon->show();
}

void XMRiGUIWindow::loadConfig() {
    QFile file(settingsPath);
    if (file.open(QIODevice::ReadOnly)) {
        QJsonDocument doc = QJsonDocument::fromJson(file.readAll());
        QJsonObject root = doc.object();
        for (int i = 0; i < 3; ++i) {
            QString id = QString("profile-%1").arg(i);
            if (root.contains(id)) {
                QJsonObject p = root[id].toObject();
                ProfileConfig& c = configs[id];
                c.mine = false;
                c.pool = p["pool"].toString();
                c.user = p["user"].toString();
                c.password = p["password"].toString();
                c.donate = p["donate"].toString();
                c.threads = p["threads"].toString();
                c.cuda = p["cuda"].toBool();
                c.opencl = p["opencl"].toBool();
                c.cpu = p["cpu"].toBool();
                c.coin = p["coin"].toInt();
                c.args = p["args"].toString();
                c.defaultArgs = p["default_args"].toBool();
            }
        }
    }
    for (int i = 0; i < 3; ++i) {
        QString id = QString("profile-%1").arg(i);
        if (!configs.contains(id)) {
            ProfileConfig c;
            c.pool = "stratum+tcp://pool.supportxmr.com:3333";
            c.user = "YOUR_WALLET";
            c.coin = 3; // Monero
            configs[id] = c;
        }
    }
}

void XMRiGUIWindow::saveConfig() {
    QJsonObject root;
    for (int i = 0; i < 3; ++i) {
        QString id = QString("profile-%1").arg(i);
        auto& ui = widgets[id];
        auto& c = configs[id];
        c.pool = ui.pool->text(); c.user = ui.user->text(); c.password = ui.pass->text();
        c.donate = ui.donate->text(); c.threads = ui.threads->text();
        c.cuda = ui.cuda->isChecked(); c.opencl = ui.opencl->isChecked(); c.cpu = ui.cpu->isChecked();
        c.coin = ui.coin->currentIndex(); c.defaultArgs = ui.noDefault->isChecked(); c.args = ui.args->text();

        QJsonObject p;
        p["pool"] = c.pool; p["user"] = c.user; p["password"] = c.password;
        p["donate"] = c.donate; p["threads"] = c.threads;
        p["cuda"] = c.cuda; p["opencl"] = c.opencl; p["cpu"] = c.cpu;
        p["coin"] = c.coin; p["default_args"] = c.defaultArgs; p["args"] = c.args;
        root[id] = p;
    }
    QFile file(settingsPath);
    if (file.open(QIODevice::WriteOnly)) file.write(QJsonDocument(root).toJson());
}

void XMRiGUIWindow::setupUI() {
    QWidget* central = new QWidget(this);
    QVBoxLayout* layout = new QVBoxLayout(central);
    tabWidget = new QTabWidget(this);
    layout->addWidget(tabWidget);

    for (int i = 0; i < 3; ++i) {
        QString id = QString("profile-%1").arg(i);
        QWidget* tab = new QWidget();
        QVBoxLayout* tLayout = new QVBoxLayout(tab);

        QHBoxLayout* hLayout = new QHBoxLayout();
        QLabel* logo = new QLabel();
        QPixmap pix(iconPath);
        if (!pix.isNull()) logo->setPixmap(pix.scaled(100, 100, Qt::KeepAspectRatio, Qt::SmoothTransformation));
        hLayout->addWidget(logo);

        QLabel* info = new QLabel("<b>XMRiGUI " + APP_VERSION + "</b><br>by Freetime Maker<br><a href='https://github.com/FreetimeMaker/XMRiGUI'>Source Code</a>");
        info->setOpenExternalLinks(true);
        hLayout->addWidget(info);
        hLayout->addStretch();

        QVBoxLayout* mBox = new QVBoxLayout();
        QPushButton* mBtn = new QPushButton("START MINING");
        mBtn->setCheckable(true); mBtn->setMinimumHeight(50);
        mBtn->setStyleSheet("QPushButton:checked { background-color: #e74c3c; color: white; font-weight: bold; } QPushButton { background-color: #2ecc71; color: white; font-weight: bold; }");

        QLabel* status = new QLabel("Status: Stopped");
        QLabel* stats = new QLabel("Speed: 0 H/s | Shares: 0/0");
        mBox->addWidget(mBtn); mBox->addWidget(status); mBox->addWidget(stats);
        hLayout->addLayout(mBox);
        tLayout->addLayout(hLayout);

        QFrame* sFrame = new QFrame(); sFrame->setFrameStyle(QFrame::StyledPanel | QFrame::Raised);
        QGridLayout* sGrid = new QGridLayout(sFrame);
        ProfileWidgets& w = widgets[id];
        w.pool = new QLineEdit(configs[id].pool); w.user = new QLineEdit(configs[id].user);
        w.pass = new QLineEdit(configs[id].password); w.donate = new QLineEdit(configs[id].donate);
        w.threads = new QLineEdit(configs[id].threads); w.args = new QLineEdit(configs[id].args);
        w.cuda = new QCheckBox("NVIDIA (CUDA)"); w.cuda->setChecked(configs[id].cuda);
        w.opencl = new QCheckBox("AMD (OpenCL)"); w.opencl->setChecked(configs[id].opencl);
        w.cpu = new QCheckBox("CPU"); w.cpu->setChecked(configs[id].cpu);
        w.noDefault = new QCheckBox("Disable Default Args"); w.noDefault->setChecked(configs[id].defaultArgs);
        w.coin = new QComboBox(); w.coin->addItems(cryptos); w.coin->setCurrentIndex(configs[id].coin);
        w.mineBtn = mBtn; w.statusLabel = status; w.statsLabel = stats;
        w.logView = new QPlainTextEdit(); w.logView->setReadOnly(true);
        w.logView->setStyleSheet("background-color: #2c3e50; color: #ecf0f1; font-family: 'Consolas', monospace;");

        sGrid->addWidget(new QLabel("Pool:"), 0, 0); sGrid->addWidget(w.pool, 0, 1);
        sGrid->addWidget(new QLabel("User:"), 1, 0); sGrid->addWidget(w.user, 1, 1);
        sGrid->addWidget(new QLabel("Password:"), 2, 0); sGrid->addWidget(w.pass, 2, 1);
        sGrid->addWidget(new QLabel("Donate %:"), 0, 2); sGrid->addWidget(w.donate, 0, 3);
        sGrid->addWidget(new QLabel("Threads:"), 1, 2); sGrid->addWidget(w.threads, 1, 3);
        QPushButton* saveBtn = new QPushButton("Save"); connect(saveBtn, &QPushButton::clicked, this, &XMRiGUIWindow::saveConfig);
        sGrid->addWidget(saveBtn, 2, 3);
        tLayout->addWidget(sFrame);

        QHBoxLayout* adv = new QHBoxLayout();
        adv->addWidget(w.cuda); adv->addWidget(w.opencl); adv->addWidget(w.cpu);
        adv->addWidget(new QLabel("Coin:")); adv->addWidget(w.coin); adv->addWidget(w.noDefault);
        tLayout->addLayout(adv);
        tLayout->addWidget(new QLabel("Extra Args:")); tLayout->addWidget(w.args);
        tLayout->addWidget(w.logView);

        tabWidget->addTab(tab, QString("Profile %1").arg(i+1));
        connect(mBtn, &QPushButton::toggled, [this, id](bool checked){ toggleMining(id, checked); });
    }
    setCentralWidget(central);
}

void XMRiGUIWindow::toggleMining(const QString& id, bool start) {
    configs[id].mine = start;
    if (start) startMining(id);
    else stopMining(id);
}

void XMRiGUIWindow::startMining(const QString& id) {
    saveConfig();
    if (processes.contains(id)) stopMining(id);
    QStringList args = getMinerCommand(id);
    QString exe = args.takeFirst();
    if (!QFile::exists(exe)) {
        log(id, "Error: Miner not found: " + exe, "#e74c3c");
        widgets[id].mineBtn->setChecked(false);
        return;
    }
    QProcess* proc = new QProcess(this);
    connect(proc, &QProcess::readyReadStandardOutput, this, &XMRiGUIWindow::handleMinerOutput);
    connect(proc, QOverload<int, QProcess::ExitStatus>::of(&QProcess::finished), this, &XMRiGUIWindow::handleMinerFinished);
    proc->setProperty("profileId", id);
    proc->start(exe, args);
    processes[id] = proc;
    widgets[id].statusLabel->setText("Status: Starting...");
    widgets[id].mineBtn->setText("STOP MINING");
}

void XMRiGUIWindow::stopMining(const QString& id) {
    if (processes.contains(id)) {
        processes[id]->terminate();
        if (!processes[id]->waitForFinished(3000)) processes[id]->kill();
        processes.remove(id);
    }
    widgets[id].statusLabel->setText("Status: Stopped");
    widgets[id].mineBtn->setText("START MINING");
}

QStringList XMRiGUIWindow::getMinerCommand(const QString& id) {
    auto& c = configs[id];
    QString coin = cryptos[c.coin];
    QStringList args;
    if (coin == "Bitcoin" || coin == "Litecoin") {
        args << cpuminerPath << "-o" << c.pool << "-u" << c.user;
        if (!c.password.isEmpty()) args << "-p" << c.password;
    } else if (coin == "Ethereum Classic") {
        args << lolminerPath << "--algo" << "ETCHASH" << "--pool" << c.pool << "--user" << c.user;
        if (!c.password.isEmpty()) args << "--pass" << c.password;
    } else {
        args << xmrigPath << "--no-color";
        if (!c.defaultArgs) {
            args << "--algo" << algos[c.coin] << "--url" << c.pool << "--user" << c.user;
            args << "--pass" << (c.password.isEmpty() ? "x" : c.password) << "--donate-level" << c.donate;
            if (c.threads != "0") args << "--threads" << c.threads << "--randomx-init" << c.threads;
            if (c.cuda) args << "--cuda" << "--cuda-loader" << cudaPluginPath;
            if (c.opencl) args << "--opencl";
            if (!c.cpu) args << "--no-cpu";
        }
    }
    if (!c.args.isEmpty()) args << c.args.split(" ");
    return args;
}

void XMRiGUIWindow::handleMinerOutput() {
    QProcess* proc = qobject_cast<QProcess*>(sender());
    if (!proc) return;
    QString id = proc->property("profileId").toString();
    QString text = QString::fromUtf8(proc->readAllStandardOutput());
    for (const QString& line : text.split("\n")) {
        if (line.trimmed().isEmpty()) continue;
        QString l = line.toLower();
        QString color = "";
        if (l.contains("accepted")) { color = "#2ecc71"; widgets[id].statusLabel->setText("Status: Mining (Share accepted!)"); }
        else if (l.contains("error") || l.contains("rejected")) color = "#e74c3c";
        else if (l.contains("net") || l.contains("pool")) color = "#3498db";
        else if (l.contains("speed")) color = "#f1c40f";
        log(id, line, color);
        static QRegularExpression spdRegex("speed 10s/60s/15m\\s+([\\d.]+)");
        static QRegularExpression shrRegex("accepted\\s+\\((\\d+)/(\\d+)\\)");
        auto mS = spdRegex.match(line); if (mS.hasMatch()) widgets[id].statsLabel->setProperty("s", mS.captured(1));
        auto mH = shrRegex.match(line); if (mH.hasMatch()) widgets[id].statsLabel->setProperty("h", mH.captured(1)+"/"+mH.captured(2));
        QString s = widgets[id].statsLabel->property("s").toString(); if (s.isEmpty()) s = "0.0";
        QString h = widgets[id].statsLabel->property("h").toString(); if (h.isEmpty()) h = "0/0";
        widgets[id].statsLabel->setText(QString("Speed: %1 H/s | Shares: %2").arg(s).arg(h));
    }
}

void XMRiGUIWindow::log(const QString& id, const QString& msg, const QString& color) {
    auto& w = widgets[id];
    QTextCharFormat fmt; if (!color.isEmpty()) fmt.setForeground(QColor(color));
    w.logView->setCurrentCharFormat(fmt); w.logView->appendPlainText(msg);
}

void XMRiGUIWindow::handleMinerFinished(int, QProcess::ExitStatus) {
    QString id = sender()->property("profileId").toString();
    stopMining(id); widgets[id].mineBtn->setChecked(false);
}

void XMRiGUIWindow::handleArgs(const QStringList& args) {
    if (args.contains("start")) for (int i=0; i<3; ++i) widgets[QString("profile-%1").arg(i)].mineBtn->setChecked(true);
    else if (args.contains("stop")) for (int i=0; i<3; ++i) widgets[QString("profile-%1").arg(i)].mineBtn->setChecked(false);
    showWindow();
}

void XMRiGUIWindow::showWindow() { show(); activateWindow(); raise(); }
void XMRiGUIWindow::quitApp() { qApp->quit(); }
void XMRiGUIWindow::trayIconActivated(QSystemTrayIcon::ActivationReason r) { if (r == QSystemTrayIcon::Trigger) showWindow(); }
void XMRiGUIWindow::checkAppUpdates() { networkManager->get(QNetworkRequest(QUrl("https://api.github.com/repos/FreetimeMaker/XMRiGUI/releases/latest"))); }
void XMRiGUIWindow::onUpdateCheckFinished(QNetworkReply* r) {
    if (r->error() == QNetworkReply::NoError) {
        QJsonObject root = QJsonDocument::fromJson(r->readAll()).object();
        QString v = root["tag_name"].toString();
        if (!v.isEmpty() && v != APP_VERSION) {
            if (QMessageBox::question(this, "Update", "New version " + v + " available. Download?", QMessageBox::Yes|QMessageBox::No) == QMessageBox::Yes)
                QDesktopServices::openUrl(QUrl(root["html_url"].toString()));
        }
    }
    r->deleteLater();
}

void XMRiGUIWindow::checkMinerUpdates() { /* XMRig update logic here */ }

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);
    app.setQuitOnLastWindowClosed(false);
    XMRiGUIWindow window;
    window.show();
    window.handleArgs(app.arguments());
    return app.exec();
}
