$scriptPath = "c:\Users\Kauê\Documents\02_Programacao_e_Tech\Projetos\TimeTabling\scripts\notify_agenda.ps1"
$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-ExecutionPolicy Bypass -WindowStyle Hidden -File `"$scriptPath`""

$exactTime = [DateTime]::ParseExact("2026-11-04 19:40:00", "yyyy-MM-dd HH:mm:ss", [System.Globalization.CultureInfo]::InvariantCulture)
$trigger = New-ScheduledTaskTrigger -Once -At $exactTime

$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -WakeToRun

Register-ScheduledTask -TaskName "Agenda_Claude_Pitch_19h40" -Action $action -Trigger $trigger -Settings $settings -Force
Get-ScheduledTaskInfo -TaskName "Agenda_Claude_Pitch_19h40" | Select-Object TaskName, NextRunTime
