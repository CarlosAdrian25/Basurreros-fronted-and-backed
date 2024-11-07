import 'package:flutter/material.dart';
import 'main.dart';

class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('BIENVENIDO:USER{USUARIO_NAME}'),
      ),
      drawer: Drawer(
        child: ListView(
          padding: EdgeInsets.zero,
          children: [
            const DrawerHeader(
              decoration: BoxDecoration(
                color: Colors.teal,
              ),
              child: Text(
                'Menú',
                style: TextStyle(
                  color: Colors.white,
                  fontSize: 24,
                ),
              ),
            ),
            ListTile(
              title: const Text('Perfil'),
              onTap: () {
                Navigator.pop(context); // Cierra el menú
                // Agrega aquí la acción que necesites para "Perfil"
              },
            ),
            ListTile(
              title: const Text('Configuraciones'),
              onTap: () {
                Navigator.pop(context); // Cierra el menú
                // Agrega aquí la acción que necesites para "Configuraciones"
              },
            ),
            ListTile(
              title: const Text('Cerrar sesión'),
              onTap: () {
                // Cierra el menú
                Navigator.pop(context);

                // Navega a la pantalla de inicio de sesión en main.dart y limpia la pila de navegación
                Navigator.pushAndRemoveUntil(
                  context,
                  MaterialPageRoute(
                      builder: (context) =>
                          const MyApp()), // Llama a `MyApp` para ir a la pantalla de inicio de sesión
                  (route) => false,
                );
              },
            ),
          ],
        ),
      ),
      body: const Center(
        child: Text(
          'Bienvenido a la nueva página',
          style: TextStyle(fontSize: 24),
        ),
      ),
    );
  }
}
