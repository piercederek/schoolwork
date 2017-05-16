package com.example.derekpierce.fitnessapp;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.Button;
import android.app.Activity;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.EditText;
import android.widget.RadioGroup;
import android.widget.RadioButton;
import android.widget.TextView;
import android.widget.Toast;

public class MainActivity extends AppCompatActivity {

    private Button mCalculate;
    private EditText mAmount;
    private RadioGroup mUnit;
    private RadioGroup mType;
    private TextView mConversion;
    private TextView mEquivalents;
    private double pushupCalRep = (double) 100 / 350;
    private double situpsCalRep = (double) 100 / 200;
    private double jjCalMin = (double) 100 / 10;
    private double joggingCalMin = (double) 100 / 12;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        mCalculate = (Button) findViewById(R.id.calculate);

        mCalculate.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                doConversion();
            }
        });

    }

    private void doConversion() {
        mAmount = (EditText) findViewById(R.id.number);
        mUnit = (RadioGroup) findViewById(R.id.unit);
        mType = (RadioGroup) findViewById(R.id.type);
        mConversion = (TextView) findViewById(R.id.conversion);
        mEquivalents = (TextView) findViewById(R.id.equivalents);

        int selectedUnit = mUnit.getCheckedRadioButtonId();
        int selectedType = mType.getCheckedRadioButtonId();
        RadioButton unit = (RadioButton) findViewById(selectedUnit);
        RadioButton type = (RadioButton) findViewById(selectedType);
        if(mAmount.getText().toString().equals("")) {
            Toast.makeText(MainActivity.this, "Please specify an amount of exercise", Toast.LENGTH_LONG).show();
            return;
        }
        int i = Integer.parseInt(mAmount.getText().toString());

        if (type == null) {
            Toast.makeText(MainActivity.this, "Please specify a type of exercise", Toast.LENGTH_LONG).show();
            return;
        } else if (type.getText().equals("Pushups")) {
            if (unit == null) {
                Toast.makeText(MainActivity.this, "If entering pushups please select reps in the unit section", Toast.LENGTH_LONG).show();
                return;
            } else if (unit.getText().equals("Minutes")) {
                Toast.makeText(MainActivity.this, "Please specify reps of pushups not minutes", Toast.LENGTH_LONG).show();
                return;
            } else {
                mConversion.setText("You burned " + Double.toString(Math.round((double) i * pushupCalRep * 100d) / 100d) + " calories!");
                mEquivalents.setText("This is equivalent to\n" + Double.toString(Math.round((double) i * pushupCalRep / situpsCalRep * 100d) / 100d) + " situps or\n" +
                        Double.toString(Math.round((double) i * pushupCalRep / jjCalMin * 100d) / 100d) + " minutes of jumping jacks or\n" +
                        Double.toString(Math.round((double) i * pushupCalRep / joggingCalMin * 100d) / 100d) + " minutes of jogging");
            }
        } else if (type.getText().equals("Situps")) {
            if (unit == null) {
                Toast.makeText(MainActivity.this, "If entering situps please select reps in the unit section", Toast.LENGTH_LONG).show();
                return;
            } else if (unit.getText().equals("Minutes")) {
                Toast.makeText(MainActivity.this, "Please specify reps of situps not minutes", Toast.LENGTH_LONG).show();
                return;
            } else {
                mConversion.setText("You burned " + Double.toString(Math.round((double) i * situpsCalRep * 100d) / 100d) + " calories!");
                mEquivalents.setText("This is equivalent to\n" + Double.toString(Math.round((double) i * situpsCalRep / pushupCalRep * 100d) / 100d) + " pushups or\n" +
                        Double.toString(Math.round((double) i * situpsCalRep / jjCalMin * 100d) / 100d) + " minutes of jumping jacks or\n" +
                        Double.toString(Math.round((double) i * situpsCalRep / joggingCalMin * 100d) / 100d) + " minutes of jogging");
            }
        } else if (type.getText().equals("Jumping Jacks")) {
            if (unit == null) {
                Toast.makeText(MainActivity.this, "If entering jumping jacks please select minutes in the unit section", Toast.LENGTH_LONG).show();
                return;
            } else if (unit.getText().equals("Reps")) {
                Toast.makeText(MainActivity.this, "Please specify minutes of jumping jacks not reps", Toast.LENGTH_LONG).show();
                return;
            } else {
                mConversion.setText("You burned " + Double.toString(Math.round((double) i * jjCalMin * 100d) / 100d) + " calories!");
                mEquivalents.setText("This is equivalent to\n" + Double.toString(Math.round((double) i * jjCalMin / pushupCalRep * 100d) / 100d) + " pushups or\n" +
                        Double.toString(Math.round((double) i * jjCalMin / situpsCalRep * 100d) / 100d) + " situps or\n" +
                        Double.toString(Math.round((double) i * jjCalMin / joggingCalMin * 100d) / 100d) + " minutes of jogging");
            }
        } else {
            if (unit == null) {
                Toast.makeText(MainActivity.this, "If entering jogging please select minutes in the unit section", Toast.LENGTH_LONG).show();
                return;
            } else if (unit.getText().equals("Reps")) {
                Toast.makeText(MainActivity.this, "Please specify minutes of jogging not reps", Toast.LENGTH_LONG).show();
                return;
            } else {
                mConversion.setText("You burned " + Double.toString(Math.round((double) i * joggingCalMin * 100d) / 100d) + " calories!");
                mEquivalents.setText("This is equivalent to\n" + Double.toString(Math.round((double) i * joggingCalMin / pushupCalRep * 100d) / 100d) + " pushups or\n" +
                        Double.toString(Math.round((double) i * joggingCalMin / situpsCalRep * 100d) / 100d) + " situps or\n" +
                        Double.toString(Math.round((double) i * joggingCalMin / jjCalMin * 100d) / 100d) + " minutes of jumping jacks");
            }
        }
    }
}
