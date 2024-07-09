#!/bin/sh

# Función para imprimir el encabezado
print_header() {
    echo   "*********************************************"
    printf "  🔍  %s\n" "$1"
    echo   "*********************************************"
}

# Test case 1: No URL provided
print_header "Test case 1: No URL provided"
./myawesomescript.sh

# Test case 2: Single URL provided
print_header "Test case 2: Single URL provided"
./myawesomescript.sh bit.ly/1O72s3U

# Test case 3: Multiple URLs provided
print_header "Test case 3: Multiple URLs provided"
./myawesomescript.sh bit.ly/1O72s3U bit.ly/3VNxdR6

# Test case 4: Invalid URL provided	
print_header "Test case 4: Invalid URL provided"
./myawesomescript.sh bit.ly/1O72sXX bit.ly/3VNxdXX
