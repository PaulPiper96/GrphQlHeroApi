import requests

class HeroGraphQLClient:
    def __init__(self, url, key):
        """
        Initialize the client with the endpoint URL and API key.
        """
        self.url = url
        self.api_key = self.read(key)
        if not self.api_key:
            raise ValueError("API key could not be read from the provided .pem file.")
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

    @staticmethod
    def read(file_path):
        """
        Reads the API key from a .pem file.

        :param file_path: Path to the .pem file.
        :return: The API key as a string.
        """
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                # Remove empty lines and extract the actual key
                key_lines = [line.strip() for line in lines if line.strip() and not line.startswith("-----")]
                return ''.join(key_lines)
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return None
        except Exception as e:
            print(f"An error occurred while reading the file: {e}")
            return None

    def execute_query(self, query, variables=None):
        """
        Execute a GraphQL query with optional variables.

        :param query: The GraphQL query string.
        :param variables: A dictionary of variables for the query.
        :return: The response data as a dictionary or None if the request fails.
        """
        payload = {"query": query}
        if variables:
            payload["variables"] = variables

        try:
            response = requests.post(self.url, json=payload, headers=self.headers)
            print("\nResponse status code (Query):", response.status_code)
            if response.status_code == 200:
                return response.json()
            else:
                print("Failed to execute query:", response.text)
                return None
        except requests.exceptions.RequestException as e:
            print("An error occurred while executing the query:", e)
            return None

    def execute_mutation(self, mutation, variables=None):
        """
        Execute a GraphQL mutation (write operation) with optional variables.

        :param mutation: The GraphQL mutation string.
        :param variables: A dictionary of variables for the mutation.
        :return: The response data as a dictionary or None if the request fails.
        """
        payload = {"query": mutation}
        if variables:
            payload["variables"] = variables

        try:
            response = requests.post(self.url, json=payload, headers=self.headers)
            print("\nResponse status code (Mutation):", response.status_code)
            if response.status_code == 200:
                return response.json()
            else:
                print("Failed to execute mutation:", response.text)
                return None
        except requests.exceptions.RequestException as e:
            print("An error occurred while executing the mutation:", e)
            return None


if __name__ == "__main__":
    # -------------------------
    # Setup
    # -------------------------
    api_url = "https://login.hero-software.de/api/external/v7/graphql"
    api_key_path = ""  # Ersetze dies durch deinen echten Pfad zur .pem-Datei

    client = HeroGraphQLClient(api_url, api_key_path)

    # ------------------------------------
    # Beispiel: Vorhandene Projekte abfragen (Query)
    # ------------------------------------
    projects_query = """
    query {
      project_matches {
        id
        project_nr
        measure {
          short
          name
        }
        customer {
          id
          first_name
          last_name
          email
        }
        contact {
          id
          first_name
          last_name
          email
        }
        address {
          street
          city
          zipcode
        }
        current_project_match_status {
          status_code
          name
        }
      }
    }
    """

    projects_response = client.execute_query(projects_query)
    print("\n--- All Projects (project_matches) ---")
    if projects_response is not None:
        print("Full response:", projects_response)
        if "data" in projects_response and projects_response["data"].get("project_matches"):
            print("Projects Data:", projects_response["data"]["project_matches"])
        else:
            print("No project data found or 'project_matches' is empty.")
    else:
        print("Failed to retrieve projects.")


    # ------------------------------------
    # Beispiel: Kontakt erstellen (Mutation)
    # ------------------------------------
    # Wir nehmen dein statisches Beispiel:
    #   mutation create_contact{
    #      create_contact(
    #         contact:{
    #            last_name:"Nachname"
    #            first_name:"Vorname"
    #            email:"emailadresse@provider.de"
    #            source:"Website"
    #            address:{
    #              street: "Göttinger Hof 9"
    #              city: "Hannover"
    #              zipcode: "30453"
    #            }
    #         }
    #      ) {
    #          id
    #      }
    #   }
    create_contact_mutation = """
    mutation {
      create_contact(
        contact: {
          first_name: "Max"
          last_name: "Mustermann"
          email: "max.mustermann@example.org"
          source: "Website"
          address: {
            street: "Göttinger Hof 9"
            city: "Hannover"
            zipcode: "30453"
          }
        }
      ) {
        id
        # Ggf. weitere Felder, wenn vorhanden:
        # first_name
        # last_name
      }
    }
    """

    # Hier senden wir die Mutation OHNE Variablen-Objekt (da alles statisch ist)
    create_contact_response = client.execute_mutation(create_contact_mutation)
    print("\n--- Create Contact (Mutation) ---")
    if create_contact_response is not None:
        print("Full mutation response:", create_contact_response)
        if "errors" in create_contact_response:
            print("\nGraphQL Errors:")
            for err in create_contact_response["errors"]:
                print(err)
        elif "data" in create_contact_response and "create_contact" in create_contact_response["data"]:
            print("\nSuccessfully created contact!")
            print("Contact ID:", create_contact_response["data"]["create_contact"]["id"])
        else:
            print("\nNo 'data' field found in the response.")
    else:
        print("Failed to create a contact.")
