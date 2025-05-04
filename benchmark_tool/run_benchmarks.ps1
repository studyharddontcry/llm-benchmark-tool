# Define arrays of models and tasks
$models = @(
    "qwen2.5-coder:3b",
    "qwen2.5-coder:7b",
    "codellama:7b",
    "llama2:7b"
)

$tasks = @{
    "fft" = "Write a function that performs FFT on a given signal and returns the frequency spectrum."
    "inverse_fft" = "Write a function that performs inverse FFT on a frequency spectrum and returns the time domain signal."
    "resampling" = "Write a function that resamples a signal to a new length using interpolation."
    "convolution" = "Write a function that performs convolution of two signals and returns the result."
    "signal_generation" = "Write a function that generates a sine wave with specified frequency, sample rate, and duration."
}

# Settings
$temperature = 0.3
$runs = 10

# Counter for progress
$total = $models.Length * $tasks.Count
$current = 0

# Run all combinations
foreach ($model in $models) {
    foreach ($taskEntry in $tasks.GetEnumerator()) {
        $current++
        $task = $taskEntry.Key
        $description = $taskEntry.Value
        
        Write-Host "`nCombination $current/$total"
        Write-Host "Model: $model"
        Write-Host "Task: $task"
        Write-Host ("-" * 40)
        
        # Run the Python script
        python runner.py `
            --task $task `
            --description $description `
            --model $model `
            --temperature $temperature `
            --runs $runs
        
        # Delay between runs
        Start-Sleep -Seconds 2
    }
}

Write-Host "`nAll combinations completed!"