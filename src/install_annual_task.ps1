param(
    [string]$Repo = "cmduyeen/lich-am-viet-nam",
    [string]$TaskName = "LunarCalendarsAnnual",
    [string]$Python = ""
)
$ErrorActionPreference = "Stop"
if ($Repo -notmatch "^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$") { throw "Repo must be owner/repository" }
$projectRoot = Split-Path -Parent $PSScriptRoot
if (-not $Python) { $Python = Join-Path $projectRoot ".venv\Scripts\python.exe" }
if (-not (Test-Path -LiteralPath $Python -PathType Leaf)) { throw "Create the project .venv before installing the task." }
$ghPath = (Get-Command gh -ErrorAction Stop).Source
$scriptPath = Join-Path $PSScriptRoot "maintenance.py"
$logPath = Join-Path $projectRoot ".maintenance.log"
# No passwords, tokens, paid services or ChatGPT runtime are stored in this task.
$taskAction = New-ScheduledTaskAction -Execute $Python -Argument "`"$scriptPath`" --repo $Repo --gh `"$ghPath`" --log-file `"$logPath`"" -WorkingDirectory $projectRoot
$taskSettings = New-ScheduledTaskSettingsSet -StartWhenAvailable -RunOnlyIfNetworkAvailable -ExecutionTimeLimit (New-TimeSpan -Minutes 5) -MultipleInstances IgnoreNew
$currentUser = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name
$taskPrincipal = New-ScheduledTaskPrincipal -UserId $currentUser -LogonType Interactive -RunLevel Limited
$task = New-ScheduledTask -Action $taskAction -Settings $taskSettings -Principal $taskPrincipal
# ScheduleByMonth provides one annual invocation on January 1 at 07:35 UTC+7.
$taskXml = [xml]($task | Export-ScheduledTask)
$nextYear = [DateTimeOffset]::Now.ToOffset([TimeSpan]::FromHours(7)).Year + 1
$annualStart = "${nextYear}-01-01T07:35:00+07:00"
$ns = $taskXml.DocumentElement.NamespaceURI
$triggers = $taskXml.CreateElement("Triggers", $ns)
$calendar = $taskXml.CreateElement("CalendarTrigger", $ns)
foreach ($pair in @(@("StartBoundary", $annualStart), @("Enabled", "true"))) {
    $element = $taskXml.CreateElement($pair[0], $ns); $element.InnerText = $pair[1]; [void]$calendar.AppendChild($element)
}
$schedule = $taskXml.CreateElement("ScheduleByMonth", $ns)
$days = $taskXml.CreateElement("DaysOfMonth", $ns); $day = $taskXml.CreateElement("Day", $ns); $day.InnerText = "1"; [void]$days.AppendChild($day)
$months = $taskXml.CreateElement("Months", $ns); [void]$months.AppendChild($taskXml.CreateElement("January", $ns))
[void]$schedule.AppendChild($days); [void]$schedule.AppendChild($months); [void]$calendar.AppendChild($schedule); [void]$triggers.AppendChild($calendar)
$old = $taskXml.DocumentElement.SelectSingleNode("*[local-name()='Triggers']")
if ($old) { [void]$taskXml.DocumentElement.ReplaceChild($triggers, $old) } else { [void]$taskXml.DocumentElement.InsertBefore($triggers, $taskXml.DocumentElement.SelectSingleNode("*[local-name()='Principals']")) }
Register-ScheduledTask -TaskName $TaskName -Xml $taskXml.OuterXml -Force | Out-Null
Get-ScheduledTaskInfo -TaskName $TaskName | Select-Object NextRunTime, LastTaskResult
