import { Text, View } from "react-native";
import React from "react";
import Pilula from "./pilula";
import Settings from "./settings";
import { NavigationContainer } from "@react-navigation/native";
import { createStackNavigator } from "@react-navigation/stack";
import Home from "./home";

const Stack = createStackNavigator();

export default function Index() {
  return (
    <NavigationContainer independent={true}>
      <Stack.Navigator initialRouteName="Home" screenOptions={{  headerTitleAlign: "center" }}>
      {/* <Stack.Navigator initialRouteName="Home" screenOptions={{ headerShown: false }}> */}
        <Stack.Screen name="Home" component={Home} />
        <Stack.Screen name="Settings" component={Settings} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
