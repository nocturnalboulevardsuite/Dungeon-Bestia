import streamlit as st

st.set_page_config(page_title="Coliseo & Mazmorra", page_icon="⚔️", layout="centered")

# ------------------------------------------------------------------------------
# 1. INICIALIZACIÓN DEL ESTADO DEL JUEGO
# ------------------------------------------------------------------------------
if "stage" not in st.session_state:
    st.session_state.stage = "COLISEUM"
if "character" not in st.session_state:
    st.session_state.character = {}
if "inventory" not in st.session_state:
    st.session_state.inventory = []

# ------------------------------------------------------------------------------
# ESCENA 1: EL COLISEO (Derrota Programada)
# ------------------------------------------------------------------------------
if st.session_state.stage == "COLISEUM":
    st.title("⚔️ El Coliseo del Olvido")
    st.write("Apenas puedes sostenerte en pie. No recuerdas quién eres ni cómo llegaste aquí.")
    st.write("Frente a ti se alza **LA BESTIA**: un gigante mutado envuelto en cadenas con un casco de metal impenetrable.")
    st.write("La multitud ruge. LA BESTIA se abalanza hacia ti.")

    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🗡️ Atacar"):
            st.session_state.knockout_reason = (
                "Le asestas un golpe con tus puños desnudos... El impacto frena contra su casco de metal. "
                "La Bestia se ríe con fuerza, levanta su enorme puño y te noquea de un solo impacto."
            )
            st.session_state.stage = "KNOCKED_OUT"
            st.rerun()

    with col2:
        if st.button("🏃 Esquivar"):
            st.session_state.knockout_reason = (
                "Intentas rodar hacia un lado, pero su sombra cubre el piso entero. "
                "Te embiste y te estrella contra la pared antes de que termines el movimiento."
            )
            st.session_state.stage = "KNOCKED_OUT"
            st.rerun()

    with col3:
        if st.button("🚪 Escapar"):
            st.session_state.knockout_reason = (
                "Das media vuelta e intentas correr a los portones. La Bestia te atrapa del cuello "
                "con una sola mano y te azota violentamente contra el suelo."
            )
            st.session_state.stage = "KNOCKED_OUT"
            st.rerun()

# ------------------------------------------------------------------------------
# ESCENA 2: PANTALLA NEGRA / DESMAYO
# ------------------------------------------------------------------------------
elif st.session_state.stage == "KNOCKED_OUT":
    st.title("🖤 Oscuridad...")
    st.error(st.session_state.knockout_reason)
    st.markdown("---")
    st.write("*Todo se vuelve negro. El rugido de la arena se apaga gradualmente hasta quedar en silencio absoluto...*")
    
    if st.button("👁️ Abrir los ojos"):
        st.session_state.stage = "MIRROR_ROOM"
        st.rerun()

# ------------------------------------------------------------------------------
# ESCENA 3: LA HABITACIÓN DEL ESPEJO (Creación de Personaje)
# ------------------------------------------------------------------------------
elif st.session_state.stage == "MIRROR_ROOM":
    st.title("🪞 La Habitación del Espejo")
    st.write("Despiertas en una habitación de piedra fría e iluminada por antorchas de fuego azul.")
    st.write("Frente a ti hay un espejo antiguo. Al acercarte, ves tu reflejo sin rostro comenzando a tomar forma...")

    with st.form("character_creation"):
        st.subheader("Personaliza tu Entidad")
        
        raza = st.selectbox("Raza:", ["Humano", "Elfo", "Vampiro", "Mobestia", "Hombre Lobo", "Mago", "Robot Ancestral"])
        color_ojos = st.selectbox("Color de Ojos:", ["Carmesí", "Azul Eléctrico", "Verde Esmeralda", "Dorado", "Negro Profundo", "Blanco Luminoso"])
        color_pelo = st.selectbox("Cabello:", ["Negro Azabache", "Blanco Plateado", "Rojo Fuego", "Calvo / Metálico", "Castaño"])
        
        col_phys1, col_phys2 = st.columns(2)
        with col_phys1:
            estatura = st.slider("Estatura (cm):", 120, 230, 175)
        with col_phys2:
            peso = st.slider("Peso (kg):", 40, 160, 70)
            
        arma_inicial = st.selectbox("Arma Inicial:", [
            "Báculo de Magia Básica",
            "Espada Corta de Hierro",
            "Arco Recurvo"
        ])

        submitted = st.form_submit_button("✨ Reclamar tu Identidad e Iniciar")
        if submitted:
            st.session_state.character = {
                "raza": raza,
                "ojos": color_ojos,
                "pelo": color_pelo,
                "estatura": estatura,
                "peso": peso,
                "arma_equipada": arma_inicial
            }
            st.session_state.inventory = [arma_inicial]
            st.session_state.stage = "DUNGEON"
            st.rerun()

# ------------------------------------------------------------------------------
# ESCENA 4: EXPLORACIÓN Y COFRES (Lógica de Items Libres)
# ------------------------------------------------------------------------------
elif st.session_state.stage == "DUNGEON":
    char = st.session_state.character
    st.title("🏰 Las Mazmorras Inferiores")
    
    # Barra lateral con estadísticas del personaje
    st.sidebar.title("👤 Ficha de Personaje")
    st.sidebar.write(f"**Raza:** {char['raza']}")
    st.sidebar.write(f"**Ojos:** {char['ojos']} | **Pelo:** {char['pelo']}")
    st.sidebar.write(f"**Físico:** {char['estatura']} cm / {char['peso']} kg")
    st.sidebar.markdown("---")
    st.sidebar.subheader("🎒 Inventario")
    for item in st.session_state.inventory:
        if item == char["arma_equipada"]:
            st.sidebar.write(f"⚡ **{item}** *(Equipada)*")
        else:
            st.sidebar.write(f"• {item}")

    st.subheader(f"Te adentras en la mazmorra como un {char['raza']}.")
    st.write(f"Llevas equipada tu **{char['arma_equipada']}**.")
    st.write("Al fondo del pasillo encuentras un cofre antiguo reforzado con runas de rayo.")

    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🧰 Abrir Cofre"):
            nueva_arma = "Espada Hechizada Eléctrica ⚡"
            if nueva_arma not in st.session_state.inventory:
                st.session_state.inventory.append(nueva_arma)
                st.success(f"¡Has encontrado una **{nueva_arma}**! Aunque seas clase/raza {char['raza']}, puedes usarla sin restricciones.")
            else:
                st.info("El cofre ya está vacío.")

    with col2:
        if len(st.session_state.inventory) > 1:
            arma_seleccionada = st.selectbox("Seleccionar arma para equipar:", st.session_state.inventory)
            if st.button("Equipar Arma"):
                st.session_state.character["arma_equipada"] = arma_seleccionada
                st.success(f"¡Has equipado: **{arma_seleccionada}**!")
                st.rerun()

    st.markdown("---")
    if st.button("🔄 Reiniciar Aventura"):
        st.session_state.clear()
        st.rerun()
