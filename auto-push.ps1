# Auto-push script - Run this in terminal to watch for changes and push automatically
# Usage: .\auto-push.ps1

$repo = "d:\spam bot"
cd $repo

Write-Host "🔍 Auto-push monitor started. Watching for changes..." -ForegroundColor Green
Write-Host "Press Ctrl+C to stop`n" -ForegroundColor Yellow

while ($true) {
    # Check for changes
    $status = & git status --porcelain
    
    if ($status) {
        Write-Host "[$(Get-Date -Format 'HH:mm:ss')] 📝 Changes detected!" -ForegroundColor Cyan
        Write-Host $status
        
        # Stage all changes
        git add .
        
        # Get commit message
        $msg = Read-Host "Enter commit message"
        
        # Commit
        git commit -m "$msg"
        
        # Push
        Write-Host "📤 Pushing to GitHub..." -ForegroundColor Cyan
        git push
        Write-Host "✅ Pushed successfully!`n" -ForegroundColor Green
    }
    
    # Check every 30 seconds
    Start-Sleep -Seconds 30
}
