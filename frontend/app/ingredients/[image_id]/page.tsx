'use client'
import { useRouter } from "next/navigation";
import React, { useEffect, useState } from "react";

interface Ingredient {
  id: number;
  name: string;
  confidence: number;
  category: string;
}

interface PageProps {
  params: Promise<{ image_id: string }>;
}


export default function IngredientsPage({ params }: PageProps) {

  const { image_id } = React.use(params);
  const [ingredients, setIngredients] = useState<Ingredient[]>([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const router = useRouter();

  useEffect(() => {
    fetch(`http://localhost:8000/api/ingredients/${image_id}`)
      .then(res => res.json())
      .then(data => {
        setIngredients(data);
        setLoading(false);
      });
  }, [image_id]);

  const updateIngredient = (index: number,field: keyof Ingredient,value: string | number) => 
    {
        const updated = [...ingredients];
        updated[index] = {...updated[index],[field]: value,
    };

    setIngredients(updated);
  };

  const deleteIngredient = (index: number) => 
    {
        const updated = [...ingredients];
        updated.splice(index, 1);
        setIngredients(updated);
  };

  const addIngredient = () => {
    setIngredients([
      ...ingredients,
      {
        id: Date.now(),
        name: "",
        confidence: 1,
        category: "",
      },
    ]);
  };
  const getRecipe = () => {

    router.push(`/recipe/${image_id}`);
  }

  const saveChanges = async () => {
    setSaving(true);

    const response = await fetch(
      `http://localhost:8000/api/ingredients/${image_id}`,
      {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(ingredients),
      }
    );

    if (response.ok) {
      alert("Ingredients saved!");
    } else {
      alert("Failed to save.");
    }

    setSaving(false);
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-screen text-xl">
        Loading ingredients...
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-zinc-100 py-12">

      <div className="max-w-5xl mx-auto bg-white rounded-xl shadow-lg p-8">

        <h1 className="text-3xl font-bold mb-2 text-black">
          Review Ingredients
        </h1>

        <p className="text-zinc-500 mb-8">
          Edit the detected ingredients before generating recipes.
        </p>

        <table className="w-full border-collapse">

          <thead>

            <tr className="bg-zinc-900 text-white">

              <th className="p-3 text-left">Ingredient</th>
              <th className="p-3 text-left">Confidence</th>
              <th className="p-3 text-left">Category</th>
              <th className="p-3 text-center">Delete</th>

            </tr>

          </thead>

          <tbody className="text-black">

            {ingredients.map((ingredient, index) => (

              <tr
                key={ingredient.id}
                className="border-b hover:bg-zinc-50"
              >

                <td className="p-3">

                  <input
                    className="border rounded-lg px-3 py-2 w-50"
                    value={ingredient.name}
                    onChange={(e) =>
                      updateIngredient(index, "name", e.target.value)
                    }
                  />

                </td>

                <td className="p-3 border rounded-lg px-3 py-2 w-28">

                  {ingredient.confidence}

                </td>

                <td className="border rounded-lg px-3 py-2 w-28">
                    <input
                    className="border rounded-lg px-3 py-2 w-50"
                    value={ingredient.category}
                    onChange={(e) =>
                      updateIngredient(index, "category", e.target.value)
                    }
                  />

                </td>

                <td className="text-center">

                  <button
                    onClick={() => deleteIngredient(index)}
                    className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg"
                  >
                    Delete
                  </button>

                </td>

              </tr>

            ))}

          </tbody>

        </table>

        <div className="flex justify-between mt-8">

          <button
            onClick={addIngredient}
            className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg"
          >
            + Add Ingredient
          </button>

          <div className="space-x-3">

            <button
            onClick={getRecipe}
            className="bg-yellow-600 hover:bg-yellow-700 text-white px-6 py-3 rounded-lg"
          >
            Get Recipe
          </button>

            <button
              disabled={saving}
              onClick={saveChanges}
              className="bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-lg"
            >
              {saving ? "Saving..." : "Save Changes"}
            </button>

          </div>

        </div>

      </div>

    </div>
  );
}
