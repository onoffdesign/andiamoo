# A fine giro notturno (01:00) e dopo il resoconto (07:30): iberna il PC, a meno che qualcuno lo stia usando davvero.
#
# Come decide (funziona anche quando il giro gira senza accesso a Windows):
#   - nessuno ha fatto l'accesso (schermata "Accedi")            -> iberna
#   - la sessione e' bloccata                                    -> iberna
#   - la sessione e' aperta ma nessuno tocca mouse o tastiera da 15 minuti -> iberna
#   - se Windows non dice da quanto non si usa il PC: iberna se il PC e' stato risvegliato dal timer della notte
#     (00:50-01:15, 02:30-02:55 o 07:20-07:45), altrimenti lo lascia acceso (qualcuno lo aveva acceso a mano)
#   - altrimenti (qualcuno sta lavorando)                         -> resta acceso
# Ogni decisione viene scritta nel log con i dati usati, per capire cosa e' successo.

$ErrorActionPreference = "Continue"
$IdleMinutes = 15

Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;

namespace Andiamo {
  public class SessionInfo {
    public string User = "";
    public bool Active;
    public int Flags = -1;          // 0 = bloccata, 1 = sbloccata, -1 = non si sa
    public double IdleMinutes = -1; // -1 = non si sa
  }

  public static class Power {
    [DllImport("kernel32.dll")] static extern uint WTSGetActiveConsoleSessionId();
    [DllImport("wtsapi32.dll", SetLastError = true)]
    static extern bool WTSQuerySessionInformation(IntPtr server, uint sessionId, int infoClass, out IntPtr buffer, out uint bytes);
    [DllImport("wtsapi32.dll")] static extern void WTSFreeMemory(IntPtr memory);

    // WTSINFOEXW letto a posizioni fisse (come in C): Level, poi WTSINFOEX_LEVEL1_W allineata a 8 byte.
    //   8 SessionId, 12 SessionState, 16 SessionFlags, 20 WinStationName[33], 86 UserName[21]
    //   128 DomainName[18], 168 LogonTime, 176 ConnectTime, 184 DisconnectTime, 192 LastInputTime, 200 CurrentTime
    public static SessionInfo Console() {
      var info = new SessionInfo();
      uint id = WTSGetActiveConsoleSessionId();
      if (id == 0xFFFFFFFF) return info;
      IntPtr buf; uint bytes;
      if (!WTSQuerySessionInformation(IntPtr.Zero, id, 25, out buf, out bytes)) return info;   // 25 = WTSSessionInfoEx
      try {
        if (bytes < 208) return info;
        info.Active = Marshal.ReadInt32(buf, 12) == 0;   // WTSActive
        info.Flags = Marshal.ReadInt32(buf, 16);
        info.User = Marshal.PtrToStringUni(new IntPtr(buf.ToInt64() + 86)) ?? "";
        if (info.User.Length > 20) info.User = info.User.Substring(0, 20);
        long lastInput = Marshal.ReadInt64(buf, 192);
        long now = Marshal.ReadInt64(buf, 200);
        if (lastInput > 0 && now > lastInput) info.IdleMinutes = (now - lastInput) / 600000000.0;   // unita' da 100 ns
      } finally { WTSFreeMemory(buf); }
      return info;
    }
  }
}
"@

function Stamp { Get-Date -Format s }

$s = $null
try { $s = [Andiamo.Power]::Console() } catch { Write-Output "$(Stamp) Stato della sessione non leggibile: $($_.Exception.Message)" }
$wake = $null
try {
    $wake = (Get-WinEvent -FilterHashtable @{ LogName = "System"; ProviderName = "Microsoft-Windows-Power-Troubleshooter"; Id = 1 } `
             -MaxEvents 1 -ErrorAction Stop).TimeCreated
} catch { }

if ($s) {
    $user = $s.User; $active = $s.Active; $flags = $s.Flags; $idle = [math]::Round($s.IdleMinutes, 1)
} else {
    # metodo di riserva se Windows non risponde: sessione aperta = explorer attivo; bloccata = LogonUI attivo
    $explorer = Get-Process -Name explorer -ErrorAction SilentlyContinue
    $logonui = Get-Process -Name LogonUI -ErrorAction SilentlyContinue
    $user = if ($explorer) { "?" } else { "" }
    $active = [bool]$explorer
    $flags = if ($logonui) { 0 } else { -1 }
    $idle = -1
}
Write-Output "$(Stamp) Sessione: utente='$user' attiva=$active stato=$flags (0 bloccata, 1 aperta, -1 ?) inattivo_da_min=$idle ultimo_risveglio=$wake"

$byTimer = $false
if ($wake -and ((Get-Date) - $wake).TotalHours -lt 4) {
    $m = $wake.Hour * 60 + $wake.Minute
    $byTimer = ($m -ge 50 -and $m -le 75) -or ($m -ge 150 -and $m -le 175) -or ($m -ge 440 -and $m -le 465)
}

$reason = $null
if (-not $user -or -not $active) { $reason = "nessuno ha fatto l'accesso" }
elseif ($flags -eq 0) { $reason = "schermo bloccato" }
elseif ($idle -ge $IdleMinutes) { $reason = "nessun uso da $idle minuti" }
elseif ($idle -lt 0 -and $byTimer) { $reason = "risvegliato dal timer della notte alle $($wake.ToString('HH:mm'))" }

if (-not $reason) {
    Write-Output "$(Stamp) Il PC e' in uso: niente ibernazione."
    exit 0
}

Write-Output "$(Stamp) Giro finito ($reason): ibernazione."
& shutdown.exe /h 2>&1 | ForEach-Object { Write-Output "$(Stamp) shutdown: $_" }
if ($LASTEXITCODE -ne 0) {
    Write-Output "$(Stamp) shutdown /h non riuscito (codice $LASTEXITCODE): provo con il metodo di riserva."
    try {
        Add-Type -AssemblyName System.Windows.Forms
        $ok = [System.Windows.Forms.Application]::SetSuspendState([System.Windows.Forms.PowerState]::Hibernate, $false, $false)
        Write-Output "$(Stamp) Ibernazione di riserva: $ok"
    } catch {
        Write-Output "$(Stamp) Ibernazione non riuscita: $($_.Exception.Message)"
    }
}
