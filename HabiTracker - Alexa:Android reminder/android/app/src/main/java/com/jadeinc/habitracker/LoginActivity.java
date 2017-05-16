package com.jadeinc.habitracker;

import android.app.Activity;
import android.graphics.Color;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.content.Intent;

import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import java.util.List;


public class LoginActivity extends Activity  {

    public static final String TAG = "LoginActivity";

    Button b1,b2;
    EditText ed1,ed2;

    TextView tx1;
    int counter = 3;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        b1 = (Button)findViewById(R.id.button);
        ed1 = (EditText)findViewById(R.id.editText);
        ed2 = (EditText)findViewById(R.id.editText2);


        b1.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if(ed1.getText().toString().equals("admin") &&
                        ed2.getText().toString().equals("admin")) {
                    Toast.makeText(getApplicationContext(),
                            "Getting your schedule up to date...",Toast.LENGTH_SHORT).show();
                    Intent i = new Intent(LoginActivity.this, HabitList.class);
                    startActivity(i);
                }else{
                    Toast.makeText(getApplicationContext(), "Wrong Credentials!",Toast.LENGTH_SHORT).show();
                }
            }
        });

    }
}
