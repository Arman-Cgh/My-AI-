class ContextOptimizer:



    @staticmethod
    def clean_text(value):

        if value is None:

            return ""

        return str(value).strip()




    @staticmethod
    def optimize(
        profile,
        memory,
        history,
        state
    ):


        clean_profile = {}


        for key, value in (profile or {}).items():

            value = ContextOptimizer.clean_text(
                value
            )


            if value:

                clean_profile[key] = value




        clean_state = {}


        for key, value in (state or {}).items():

            if isinstance(value, dict):

                if value:

                    clean_state[key] = value


            else:

                value = ContextOptimizer.clean_text(
                    value
                )


                if value:

                    clean_state[key] = value




        clean_history = []


        for item in history or []:


            content = ContextOptimizer.clean_text(
                item.get("content")
            )


            if content:


                clean_history.append({

                    "role": item.get(
                        "role",
                        "user"
                    ),

                    "content": content

                })



        return {


            "profile": clean_profile,


            "memory": ContextOptimizer.clean_text(
                memory
            ),


            "history": clean_history[-8:],


            "state": clean_state

        }