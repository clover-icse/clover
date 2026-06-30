int main(){
    int x, y, z;

    // pre-conditions
    x = 0;
    y = 8000;
    z = 0;


    // loop body
    while(unknown()){
        if(x >= 8000){
            y = y + 1;
            z = z -1;
        }else{
            y = y - 1;
            z = z + 1;
        }

        x = x + 1;
    }

    // post-condition
    if(x == 16000){
        assert((y == 8000) && (z == 0));
    }
    
}