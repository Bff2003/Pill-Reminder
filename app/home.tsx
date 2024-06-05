import { Text, View, Button } from "react-native";
import React from "react";
import Pilula from "./pilula";

export default function Home({ navigation }: { navigation: any }) {
  let hoje = new Date();
  
  let incio = new Date(2024, 4, 28);
  let pilula = new Pilula(incio, 21, 7);

  return (
    <View
      style={{
        flex: 1,
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <Text>{"Dia de tomar a pílula: " + pilula.diaDeTomarPilula(hoje)}</Text>
      <Text>{"Incio da Pilula: " + incio.toLocaleDateString()}</Text>
      <Text>{"Ultimo dia de tomar a pílula: " + pilula.getUltimoDiaPilula().toLocaleDateString()}</Text>
      <Text>{"Inicio da pausa: " + pilula.getInicioPausa().toLocaleDateString()}</Text>
      <Text>{"Fim da pausa: " + pilula.getFimPausa().toLocaleDateString()}</Text>
      <Text>{"Inicio da proxima pilula: " + pilula.getInicioProximaPilula().toLocaleDateString()}</Text>
      
      <Button title="Configurações" onPress={() => {
        navigation.navigate("Settings");

      }} />
    </View>
  );
}
