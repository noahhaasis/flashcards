#!/usr/bin/env fish

# Parse the CSV and loop through each line, skipping the header
tail -n +2 ./cards/migrations/cards.csv | while read -l line
    # Extract the necessary fields
    set id (echo $line | cut -d ',' -f 1)
    set turkish (echo $line | cut -d ',' -f 3 | tr -d '"')
    set image_name (echo $line | cut -d ',' -f 4)
    
    # Extract the filename without extension to use as prefix
    set prefix (echo $image_name | sed 's/\.[^.]*$//')
    
    # Create output filename
    set output_file "$prefix-tk.mp3"
    
    # Print progress
    echo "Processing: $turkish → $output_file"
    
    # Make API call
    curl -X POST "https://api.elevenlabs.io/v1/text-to-speech/9BWtsMINqrJLrRacOk9x?output_format=mp3_44100_128" \
        -H "xi-api-key: sk_7ca815f07f3ad63a426c062c5905b45c142688d59912e303" \
        -H "Content-Type: application/json" \
        -d "{
            \"text\": \"$turkish\",
            \"model_id\": \"eleven_multilingual_v2\"
        }" > $output_file
    
    # Wait a short time between requests to avoid rate limiting
    sleep 1
end

echo "All pronunciations generated successfully!"
