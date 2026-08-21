#pragma once

#include <QMainWindow>
#include <QString>
#include <QNetworkAccessManager>
#include <QNetworkReply>
#include <QProcess>
#include <QMap>
#include <QJsonObject>
#include <QLineEdit>
#include <QCheckBox>
#include <QComboBox>
#include <QPushButton>
#include <QPlainTextEdit>
#include <QLabel>
#include <QTabWidget>
#include <QSystemTrayIcon>
#include <QMenu>

const QString APP_VERSION = "v1.8.0";

struct ProfileConfig {
    bool mine = false;
    QString pool;
    QString user;
    QString password;
    QString donate = "1";
    QString threads = "0";
    bool cuda = false;
    bool opencl = false;
    bool cpu = true;
    int coin = 0;
    QString args;
    bool defaultArgs = false;
};

class XMRiGUIWindow : public QMainWindow {
    Q_OBJECT
public:
    XMRiGUIWindow(QWidget *parent = nullptr);
    ~XMRiGUIWindow();

    void handleArgs(const QStringList& args);

private slots:
    void checkAppUpdates();
    void onUpdateCheckFinished(QNetworkReply* reply);
    void checkMinerUpdates();
    void onMinerDownloadFinished(QNetworkReply* reply);

    void toggleMining(const QString& profileId, bool start);
    void saveConfig();
    void handleMinerOutput();
    void handleMinerFinished(int exitCode, QProcess::ExitStatus exitStatus);

    void trayIconActivated(QSystemTrayIcon::ActivationReason reason);
    void showWindow();
    void quitApp();

private:
    void setupUI();
    void setupTray();
    void loadConfig();
    void loadPaths();
    void startMining(const QString& profileId);
    void stopMining(const QString& profileId);
    QStringList getMinerCommand(const QString& profileId);
    void log(const QString& profileId, const QString& message, const QString& color = "");

    QNetworkAccessManager* networkManager;
    QTabWidget* tabWidget;
    QSystemTrayIcon* trayIcon;

    QString settingsPath;
    QString xmrigPath;
    QString cpuminerPath;
    QString lolminerPath;
    QString cudaPluginPath;
    QString iconPath;

    QMap<QString, ProfileConfig> configs;
    QMap<QString, QProcess*> processes;

    struct ProfileWidgets {
        QLineEdit *pool, *user, *pass, *donate, *threads, *args;
        QCheckBox *cuda, *opencl, *cpu, *noDefault;
        QComboBox *coin;
        QPushButton *mineBtn;
        QLabel *statusLabel, *statsLabel;
        QPlainTextEdit *logView;
    };
    QMap<QString, ProfileWidgets> widgets;

    QStringList cryptos;
    QStringList algos;
};
