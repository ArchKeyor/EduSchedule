# Script de Notificação de Agenda para o Windows
Add-Type -AssemblyName System.Windows.Forms

# 1. Tentar exibir notificação nativa do Windows (Toast)
try {
    [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
    [Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType = WindowsRuntime] | Out-Null

    $xmlText = @"
<toast scenario="reminder">
    <visual>
        <binding template="ToastGeneric">
            <text>📅 LEMBRETE DE AGENDA (19:40)</text>
            <text>Hora de voltar ao Claude para terminar os slides do pitch para sexta e fazer o roteiro!</text>
            <text placement="attribution">Agenda Pessoal</text>
        </binding>
    </visual>
    <audio src="ms-winsoundevent:Notification.Reminder" loop="false"/>
</toast>
"@

    $xmlDoc = New-Object Windows.Data.Xml.Dom.XmlDocument
    $xmlDoc.LoadXml($xmlText)
    $toast = [Windows.UI.Notifications.ToastNotification]::new($xmlDoc)
    $appId = "{1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}\WindowsPowerShell\v1.0\powershell.exe"
    $notifier = [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier($appId)
    $notifier.Show($toast)
} catch {
    # Em caso de qualquer falha na API de Toast, o fallback garante a visualização
}

# 2. Exibir janela de diálogo visível e com foco (MessageBox) para garantir que ele veja mesmo se o Toast passar despercebido
[System.Windows.Forms.MessageBox]::Show(
    "Hora de voltar ao Claude para terminar os slides do pitch para sexta-feira e fazer o roteiro!`n`nHorário programado: 19:40",
    "AGENDA: Claude - Slides do Pitch e Roteiro",
    [System.Windows.Forms.MessageBoxButtons]::OK,
    [System.Windows.Forms.MessageBoxIcon]::Information
)
