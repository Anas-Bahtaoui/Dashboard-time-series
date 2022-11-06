from dash.dependencies import Input, Output, State
import pickle

from app import app

@app.callback(
        [Output("total", "value"),
        Output("e1", "value"),
        Output("e2", "value"),
        Output("e3", "value"),
        Output("e4", "value"),
        Output("e5", "value"),
        Output("tt-total", "value"),
        Output("tt-e1", "value"),
        Output("tt-e2", "value"),
        Output("tt-e3", "value"),
        Output("tt-e4", "value"),
        Output("tt-e5", "value")],

        [Input("save-button", "n_clicks"),
        Input("reinit-button", "n_clicks")],

        [State("total", "value"),
        State("e1", "value"),
        State("e2", "value"),
        State("e3", "value"),
        State("e4", "value"),
        State("e5", "value"),
        State("tt-total", "value"),
        State("tt-e1", "value"),
        State("tt-e2", "value"),
        State("tt-e3", "value"),
        State("tt-e4", "value"),
        State("tt-e5", "value")]
    )

def update_output(save, reinit, *states):
    try:
        with open('./s_files/old.pkl', 'rb') as f:
            old = pickle.load(f)

        if old[0] == None: old[0] = 0
        if old[1] == None: old[1] = 0

        print("old : {}".format(old))
        print("new : {}".format([save, reinit]))
        if save > old[0]:
            with open('./s_files/states.pkl', 'wb') as f:
                pickle.dump(states, f)

        if reinit > old[1]:
            with open('./s_files/states.pkl', 'wb') as f:
                pickle.dump(states, f)
            states = [0] * 12

    except:
        with open('./s_files/old.pkl', 'wb') as f:
            pickle.dump([save, reinit], f)
    return states

    # elif (reinit > reinit_clics):
    #     reinit_clics += 1
    #     return "{}, {}, {}, {}, {}".format(save_clics, save, reinit_clics, reinit, states)