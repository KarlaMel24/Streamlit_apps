# Credit: This app is inspired by Chanin Nantasenamat (Data Professor) https://youtube.com/dataprofessor


# To create interactive web applications
import streamlit as st
# To make interactive molecular visualizations
# and to display molecular structures
from stmol import showmol
# For molecular structures in 3D
import py3Dmol
# To make HTTP requiest
import requests
# Computational molecular biology
import biotite.structure.io as bsio

# Side bar and its description
st.sidebar.title('ESMFold')
st.sidebar.write("This predictor is limited to 400 aminoacids")

# stmol
def render_mol(pdb):
    # To avoid bugs or errors
    if not pbd:
        raise ValueError("Invalid PBD object")
    # New variable pbdview that creates a 3D viewer model
    pdbview = py3Dmol.view()
    # Adds the pbd model to the viewer
    pdbview.addModel(pdb,'pdb')
    pdbview.setStyle({'stick':{'color':'spectrum'}})
    pdbview.setBackgroundColor('black')
    pdbview.zoomTo()
    pdbview.zoom(2, 800) #Zoom in
    pdbview.spin(True) # Spining
    showmol(pdbview, height = 500,width=800) # Size

# Protein sequence input, the DEFAULT_SEQ is G protein [Glycine max], CAA64834.1
DEFAULT_SEQ = "MGLLCSRNRRYNDADAEENAQTAEIERRIEVRNERAEKHIQKLLLLGAGESGKSTIFKQIKLLFQTGFDEAELKSYLPVIHANVYQTIKLLHDGSKEFAQNDVDSSKYVISNENKEIGEKLLEIGGRLDYPYLSKELAQEIENLWKDPAIQETYARGSELQIPDCTDYFMENLQRLSDANYVPTKEDVLYARVRTTGVVEIQFSPVGENKKSDEVYRLFDVGGQRNERRKWIHLFEGVSAVIFCAAISEYDQTLFEDENRNRMMETKELFEWILKQPCFEKTSFMLFLNKFDIFEKKILKVPLNVCEWFKDYQPVSTGKQEIEHAYEFVKKKFEESYFQSTAPDRVDRVFKIYRTTALDQKVVKKTFKLVDETLRRRNLLEAGLL"
txt = st.sidebar.text_area('Input sequence', DEFAULT_SEQ, height=350)

# ESMfold
def update(sequence=txt):
    # Content-Type tells what kind of data is sending the client to the server
    # "application/x-www-form-urlencoded" is to send alfanumeric data
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    # POST resquest a server to accept the data enclossed in the body of the request message
    # "https://api.esmatlas.com/foldSequence/v1/pdb/" this URL is where ESMFold API returns the 3D structures
    response = requests.post('https://api.esmatlas.com/foldSequence/v1/pdb/', headers=headers, data=sequence)
    name = sequence[:3] + sequence[-3:] # Name with the first 3 and last 3 letters of the seq
    pdb_string = response.content.decode('utf-8') # Decodes from bytes to string

    # Open file in write mode
    with open('predicted.pdb', 'w') as f:
        f.write(pdb_string) #writes pdb_string in file "f"

    struct = bsio.load_structure('predicted.pdb', extra_fields=["b_factor"]) # Loads structure and b_value
    b_value = round(struct.b_factor.mean(), 4) # Calculates b_value

    # Display protein structure
    st.subheader('Visualization of predicted protein structure')
    render_mol(pdb_string)

    # plDDT value is stored in the B-factor field
    st.subheader('plDDT')
    st.write('plDDT is a per-residue estimate of the confidence in prediction on a scale from 0-100.')
    st.info(f'plDDT: {b_value}')

    st.download_button(
        label="Download PDB",
        data=pdb_string,
        file_name='predicted.pdb',
        mime='text/plain',
    )

predict = st.sidebar.button('Predict', on_click=update) # Predict button


if not predict:
    st.warning('👈 Enter protein sequence data!')
