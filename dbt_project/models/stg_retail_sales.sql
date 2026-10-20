{{ config(materialized='table') }}
with source as (
    select * from `project-gcp-510710.dbt_proj.retail_sales_bronze`
),

deduplicated as (
    select
        *,
        row_number() over (
            partition by Transaction_ID 
            order by Order_Date desc
        ) as row_num
    from source
)

select
    -- Identifiants
    cast(Transaction_ID as string) as transaction_id,
    cast(Order_ID as string) as order_id,
    cast(Customer_ID as string) as customer_id,

    -- Informations Client (avec gestion des NULLs et âges aberrants)
    coalesce(trim(Customer_Name), 'Inconnu') as customer_name,
    case 
        when Customer_Age >= 12 and Customer_Age <= 100 then cast(Customer_Age as int64)
        else null 
    end as customer_age,
    coalesce(trim(Customer_Gender), 'Non spécifié') as customer_gender,
    coalesce(trim(Customer_Segment), 'Standard') as customer_segment,

    -- Dates & Ventes
    parse_date('%Y-%m-%d', Order_Date) as order_date,
    cast(Order_Year as int64) as order_year,
    coalesce(trim(Sales_Channel), 'Inconnu') as sales_channel,

    -- Produits & Magasin
    cast(Store_ID as string) as store_id,
    coalesce(trim(Store_Name), 'Non renseigné') as store_name,
    coalesce(trim(Country), 'Inconnu') as country,
    coalesce(trim(Region), 'Inconnue') as region,
    coalesce(trim(City), 'Inconnue') as city,
    cast(Product_ID as string) as product_id,
    coalesce(trim(Product_Name), 'Produit Inconnu') as product_name,
    coalesce(trim(Product_Category), 'Autre') as product_category,
    coalesce(trim(Product_Subcategory), 'Autre') as product_subcategory,

    -- Métriques Financières (Filtre sur Quantité > 0)
    cast(Quantity as int64) as quantity,
    cast(Unit_Price as numeric) as unit_price,
    cast(Discount_Percentage as numeric) as discount_percentage,
    cast(Sales_Amount as numeric) as sales_amount,
    cast(Cost_Amount as numeric) as cost_amount,
    cast(Profit as numeric) as profit,

    -- Informations Complémentaires
    coalesce(trim(Payment_Method), 'Non spécifié') as payment_method,
    coalesce(trim(Order_Status), 'Inconnu') as order_status,
    coalesce(trim(Shipping_Method), 'Standard') as shipping_method,
    cast(Delivery_Days as int64) as delivery_days,
    coalesce(trim(Return_Flag), 'N') as return_flag,
    coalesce(trim(Return_Reason), 'Aucune') as return_reason,
    coalesce(trim(Promotion_Code), 'AUCUN') as promotion_code,
    cast(Customer_Rating as numeric) as customer_rating,
    cast(Inventory_Level as int64) as inventory_level

from deduplicated
where row_num = 1          -- Suppression des doublons
  and Quantity > 0         -- Exclusion des quantités négatives/erronées