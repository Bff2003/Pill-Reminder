import { Text, View, Button, TextInput } from "react-native";
import DateTimePickerAndroid from "@react-native-community/datetimepicker";
import React, { useState } from "react";
import AsyncStorage from "@react-native-async-storage/async-storage"
import JSON from "json5"

export default function Settings({ navigation }: { navigation: any }) {
    const [date, setDate] = useState(new Date())
    const [duracaoPilula, setDuracaoPilula] = useState(21)
    const [duracaoPausa, setDuracaoPausa] = useState(7)
    const [open, setOpen] = useState(false)

    async function loadData() {
        try {
            const value = await AsyncStorage.getItem("data")
            if (value !== null) {
                const data = JSON.parse(value)
                setDate(new Date(data.inicio_pilula))
                setDuracaoPilula(data.duracao_pilula)
                setDuracaoPausa(data.duracao_pausa)
            }

        } catch (e) {
            console.error(e)
        }
    }

    loadData()
        
    async function saveData() {
        try {
            let data = {
                inicio_pilula: date,
                duracao_pilula: duracaoPilula,
                duracao_pausa: duracaoPausa
            }
            await AsyncStorage.setItem("data", JSON.stringify(data)) 
        } catch (e) {
            console.error(e)
        }
    }

    return (
        <View
            style={{
                flex: 1,
                justifyContent: "center",
                alignItems: "center",
            }}
        >
            <Text>Pagina de Configurações</Text>
            <Text onPress={() => setOpen(true)}>{"Incio da Pilula: " + date.toLocaleDateString()}</Text>
            {open && <DateTimePickerAndroid value={date} mode="date" onChange={(event, selectedDate) => {
                setOpen(false)
                setDate(selectedDate || date)
            }} />}
            <View style={{ flexDirection: "row", alignItems: "center" }}>
                <Text style={{ marginRight: 10 }}>Duração da Pilula:</Text>
                <TextInput placeholder="Duração da Pilula" keyboardType="numeric" defaultValue={duracaoPilula.toString()} />
            </View>
            <View style={{ flexDirection: "row", alignItems: "center", marginTop: 10 }}>
                <Text style={{ marginRight: 10 }}>Duração da Pausa:</Text>
                <TextInput placeholder="Duração da Pausa" keyboardType="numeric" defaultValue={duracaoPausa.toString()} />
            </View>
            <Button title="Cancelar" onPress={() => {
                navigation.navigate("Home");
            }} />
            <Button title="Salvar" onPress={async () => {
                console.log("Salvando...");
                await saveData()

                navigation.navigate("Home");
            }} />
        </View>
    );
}
