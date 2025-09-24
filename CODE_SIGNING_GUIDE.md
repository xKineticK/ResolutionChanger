# Guía para Firma Digital de Código

## ¿Por qué Windows marca el ejecutable como sospechoso?

- Los ejecutables sin firmar son tratados como "desconocidos"
- PyInstaller empaqueta muchos archivos, lo que puede parecer sospechoso
- Windows SmartScreen bloquea ejecutables sin reputación

## Opciones de Firma Digital:

### Opción 1: Certificado EV Code Signing (~$300/año)
- **Ventajas**: Reputación inmediata, no aparece advertencia
- **Proveedores**: DigiCert, GlobalSign, Sectigo
- **Proceso**: Verificación de identidad empresarial

### Opción 2: Certificado Code Signing estándar (~$100/año)
- **Ventajas**: Más económico
- **Desventajas**: Necesita "reputación" con el tiempo
- **Proveedores**: Sectigo, SSL.com

### Opción 3: Alternativas gratuitas/temporales
- Distribuir código fuente para que usuarios compilen
- Enviar a Microsoft para análisis de SmartScreen
- Usar plataformas de distribución (Microsoft Store)

## Comando para firmar (después de obtener certificado):
```bash
signtool sign /f certificate.p12 /p password /t http://timestamp.digicert.com ResolutionChanger.exe
```