Comandos PowerShell para endpoints

1. Registro de usuario:
$response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/register/" -Method POST -Headers @{ "Content-Type" = "application/json" } -Body '{"username": "nuevo_usuario", "password": "tu_contraseña"}'
$response

2. Iniciar sesión:
$response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/login/" -Method POST -Headers @{ "Content-Type" = "application/json" } -Body '{"username": "nuevo_usuario", "password": "tu_contraseña"}'
$token = $response.access_token
Write-Output "El token es: $token"

3. Crear una nueva mascota:
$petData = @{
    name = "Firulais"
    type = "Perro"
    color = "Marrón"
    mood = "Excited"
    energy_level = 80
}
$petJson = $petData | ConvertTo-Json
$response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/pets/" -Method POST -Headers @{ "Content-Type" = "application/json"; "Authorization" = "Bearer $token" } -Body $petJson
$response

4. Listar todas las mascotas del usuario:
$response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/pets/" -Method GET -Headers @{ "Authorization" = "Bearer $token" }
$response

5. Actualizar una mascota existente:
$updatedPetData = @{
    name = "Firulais"
    type = "Perro"
    color = "Negro"
    mood = "Happy"
    energy_level = 90
}
$updatedPetJson = $updatedPetData | ConvertTo-Json
$response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/pets/Firulais" -Method PUT -Headers @{ "Content-Type" = "application/json"; "Authorization" = "Bearer $token" } -Body $updatedPetJson
$response

6. Eliminar una mascota:
$response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/pets/Firulais" -Method DELETE -Headers @{ "Authorization" = "Bearer $token" }
$response