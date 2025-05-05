# Define arrays of models and tasks
$models = @(
    "qwen2.5:3b",
    "qwen2.5-coder:3b",
    "qwen2.5-coder:7b",
    "granite-code:3b",
    "granite-code:8b"
)

$tasks = @{
    "fft" = "Write a function that performs FFT on a given signal and returns the frequency spectrum. Parameters: signal : numpy.ndarray - Input signal (1D array) to be transformed. Must be converted to float type. Returns: numpy.ndarray - FFT of the input signal with the same length as input. Use numpy library."
    "inverse_fft" = "Write a function that performs inverse FFT on a frequency spectrum and returns the time domain signal. Parameters: spectrum : numpy.ndarray - Input spectrum (complex array). Returns: numpy.ndarray - Inverse FFT of the input spectrum. Use numpy library."
    "resampling" = "Write a function that resamples a signal to a new length. Parameters: input_signal : numpy.ndarray - Input signal to resample, new_length : int - Desired length of output signal. Returns: numpy.ndarray - Resampled signal. Use scipy library."
    "convolution" = "Write a function that performs convolution of two signals. Parameters: signal : numpy.ndarray - Input signal array, kernel : numpy.ndarray - Convolution kernel. Returns: numpy.ndarray - Full convolution result. Use numpy library."
    "signal_generation" = "Write a function that generates a sine wave. Parameters: frequency : float - Frequency in Hz, sample_rate : float - Sampling rate in Hz, duration : float - Duration in seconds. Returns: numpy.ndarray - Array containing the generated sine wave samples."
    "low_pass_filter" = "Write a function that applies a low-pass Butterworth filter to a signal. Parameters: input_signal : numpy.ndarray - Input signal array, fs : float - Sampling frequency in Hz, cutoff_freq : float - Cutoff frequency in Hz, order : int - Filter order. Returns: numpy.ndarray - Filtered signal. Use scipy.signal library."
}

# Settings
$temperature = 0.6
$runs = 10

# Counter for progress
$total = $models.Length * $tasks.Count
$current = 0

# Set working directory to script location
Set-Location $PSScriptRoot

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